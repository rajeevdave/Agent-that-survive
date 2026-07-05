"""
Chapter 2: Routing — Minimal Example

Demonstrates intent-based routing using a cheap classifier model
and specialist handlers per intent.

Book reference: Gap 2 (Framework Bias) — Routing pattern shown in LangGraph,
OpenAI SDK, Semantic Kernel. Gap 3 (Isolation) — Routing must see conversation
history for follow-up accuracy.

Run:
    python chapters/02-routing/minimal/main.py
"""
from __future__ import annotations

import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../src"))

from agentic_patterns.llm.providers.base import Message
from agentic_patterns.llm.providers.factory import create_provider, create_router_provider
from agentic_patterns.memory.conversation_memory import ConversationMemory
from agentic_patterns.routing.intent_classifier import IntentClassifier
from agentic_patterns.utils.logging.logger import get_logger

logger = get_logger(__name__)

INTENTS = ["billing", "order_status", "returns", "technical", "general"]
INTENT_DESCRIPTIONS = {
    "billing":      "Payment issues, invoices, charges, subscription questions",
    "order_status": "Order tracking, delivery updates, shipping queries",
    "returns":      "Return requests, refunds, damaged items",
    "technical":    "Product issues, setup help, technical errors",
    "general":      "Anything else",
}

SPECIALIST_PROMPTS = {
    "billing":      "You are a billing specialist. Help with payment and invoice queries.",
    "order_status": "You are an order tracking specialist. Provide accurate delivery information.",
    "returns":      "You are a returns specialist. Handle returns and refunds fairly.",
    "technical":    "You are a technical support specialist. Diagnose and solve product issues.",
    "general":      "You are a helpful customer support agent.",
}


def route_and_respond(
    user_message: str,
    memory: ConversationMemory,
    router_llm=None,
    executor_llm=None,
) -> dict:
    """Route a message and generate a specialist response."""
    router_llm = router_llm or create_router_provider()
    executor_llm = executor_llm or create_provider()

    classifier = IntentClassifier(
        provider=router_llm,
        intents=INTENTS,
        intent_descriptions=INTENT_DESCRIPTIONS,
    )

    # Classifier uses conversation history for follow-up accuracy
    intent_result = classifier.classify(user_message, memory.messages)
    logger.info(
        "intent_classified",
        intent=intent_result.intent,
        confidence=intent_result.confidence,
    )

    # Track category changes (for escalation logic)
    last_intent = memory.recall("last_intent")
    if last_intent and last_intent != intent_result.intent:
        changes = memory.recall("intent_changes", 0) + 1
        memory.remember("intent_changes", changes)
    memory.remember("last_intent", intent_result.intent)

    system_prompt = SPECIALIST_PROMPTS[intent_result.intent]
    memory.add_user_message(user_message)
    messages = memory.get_messages_for_model(system_prompt)

    response = executor_llm.complete(messages=messages, max_tokens=300)
    memory.add_assistant_message(response.content)

    return {
        "response": response.content,
        "intent": intent_result.intent,
        "confidence": intent_result.confidence,
    }


if __name__ == "__main__":
    memory = ConversationMemory(session_id="demo-session")
    test_messages = [
        "Hi, my order hasn't arrived yet.",
        "It's order number 12345.",
        "Can I also ask about my invoice?",
    ]

    for msg in test_messages:
        print(f"\nUser: {msg}")
        try:
            result = route_and_respond(msg, memory)
            print(f"Intent: {result['intent']} (confidence: {result['confidence']:.0%})")
            print(f"Agent: {result['response']}")
        except Exception as exc:
            print(f"Error: {exc}")
            print("Tip: Configure API keys in .env")
            break
