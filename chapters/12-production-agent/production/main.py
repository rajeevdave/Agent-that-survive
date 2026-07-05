"""
Chapter 12: Production Agent — Complete Implementation

The full customer support agent combining all patterns simultaneously:
Routing + Memory + Tool Use + Exception Handling + Guardrails + HITL

Book reference: Gap 3 (Isolation Problem) — six patterns working together.
This is the capstone chapter the book never showed.

Run:
    python chapters/12-production-agent/production/main.py
"""
from __future__ import annotations

import json
import os
import sys
import uuid

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../src"))

from agentic_patterns.guardrails.checker import GuardrailChecker
from agentic_patterns.llm.providers.base import Message, ToolDefinition
from agentic_patterns.llm.providers.factory import create_provider, create_router_provider
from agentic_patterns.memory.conversation_memory import ConversationMemory, InMemorySessionStore
from agentic_patterns.routing.intent_classifier import IntentClassifier
from agentic_patterns.telemetry.metrics import MetricsCollector
from agentic_patterns.utils.logging.logger import get_logger

logger = get_logger(__name__)

# ── Tool definitions ──────────────────────────────────────────────────────────
SUPPORT_TOOLS = [
    ToolDefinition(
        name="get_order_status",
        description="Get the current status and tracking info for a customer order",
        parameters={
            "type": "object",
            "properties": {
                "order_id": {"type": "string", "description": "The order ID"},
                "customer_email": {"type": "string", "description": "Customer email for verification"},
            },
            "required": ["order_id", "customer_email"],
        },
    ),
    ToolDefinition(
        name="get_customer_account",
        description="Get customer account details including tier and order history",
        parameters={
            "type": "object",
            "properties": {
                "customer_email": {"type": "string", "description": "Customer email address"},
            },
            "required": ["customer_email"],
        },
    ),
    ToolDefinition(
        name="search_knowledge_base",
        description="Search the support knowledge base for relevant articles",
        parameters={
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"},
                "limit": {"type": "integer", "description": "Max results to return", "default": 3},
            },
            "required": ["query"],
        },
    ),
]

# ── Mock tool implementations ─────────────────────────────────────────────────
_MOCK_ORDERS = {
    "12345": {"status": "in_transit", "carrier": "FedEx", "tracking": "FX789456",
              "expected_delivery": "2026-07-06", "items": ["Wireless Headphones"]},
    "99876": {"status": "delivered", "delivered_on": "2026-06-25",
              "items": ["Phone Case"], "value": 12.99},
}
_MOCK_ACCOUNTS = {
    "jane@example.com": {"name": "Jane Smith", "tier": "premium",
                          "refunds_this_year": 1, "total_orders": 23},
}
_MOCK_KB = [
    {"id": "kb001", "title": "Return Policy", "content": "Returns accepted within 30 days of purchase."},
    {"id": "kb002", "title": "Shipping Times", "content": "Standard shipping takes 3-5 business days."},
    {"id": "kb003", "title": "Refund Process", "content": "Refunds are processed within 5-7 business days."},
]


def get_order_status(order_id: str, customer_email: str) -> dict:
    order = _MOCK_ORDERS.get(order_id)
    if not order:
        return {"found": False, "error": f"Order {order_id} not found"}
    return {"found": True, "order_id": order_id, **order}


def get_customer_account(customer_email: str) -> dict:
    account = _MOCK_ACCOUNTS.get(customer_email.lower())
    if not account:
        return {"found": False, "error": "Account not found"}
    return {"found": True, "email": customer_email, **account}


def search_knowledge_base(query: str, limit: int = 3) -> dict:
    query_lower = query.lower()
    results = [
        kb for kb in _MOCK_KB
        if any(word in kb["content"].lower() or word in kb["title"].lower()
               for word in query_lower.split())
    ]
    return {"results": results[:limit], "total": len(results)}


TOOL_FUNCTIONS = {
    "get_order_status": get_order_status,
    "get_customer_account": get_customer_account,
    "search_knowledge_base": search_knowledge_base,
}

INTENTS = ["order_status", "returns", "billing", "technical", "general", "escalate"]
INTENT_DESCRIPTIONS = {
    "order_status": "Tracking, delivery, shipping queries",
    "returns":      "Returns, refunds, damaged items",
    "billing":      "Payment, invoice, subscription issues",
    "technical":    "Product setup, technical issues",
    "escalate":     "Very angry customer, legal threats, complex complaints",
    "general":      "General questions",
}
SPECIALIST_PROMPTS = {
    "order_status": "You are an order tracking specialist. Always use get_order_status before discussing orders.",
    "returns":      "You are a returns specialist. Check customer_account before discussing refunds. Premium customers with <3 refunds/year can get approved refunds.",
    "billing":      "You are a billing specialist. Look up customer account details for billing queries.",
    "technical":    "You are a technical support specialist. Ask clarifying questions and provide step-by-step guidance.",
    "general":      "You are a helpful customer support agent.",
    "escalate":     "You are a senior support specialist handling a complex situation. Be empathetic and professional.",
}

ESCALATION_TRIGGERS = [
    "speak to a manager", "legal action", "lawyer", "lawsuit",
    "this is disgusting", "never shopping here again", "terrible service",
]


class ProductionSupportAgent:
    """
    Full production customer support agent.
    Combines: Routing, Memory, Tool Use, Exception Handling, Guardrails, HITL.
    """

    def __init__(
        self,
        customer_email: str,
        router_llm=None,
        executor_llm=None,
        metrics: MetricsCollector | None = None,
    ) -> None:
        self.customer_email = customer_email
        self._router = router_llm or create_router_provider()
        self._executor = executor_llm or create_provider()
        self._metrics = metrics or MetricsCollector()
        self._guardrails = GuardrailChecker()
        self._classifier = IntentClassifier(
            provider=self._router,
            intents=INTENTS,
            intent_descriptions=INTENT_DESCRIPTIONS,
        )
        self._session_store = InMemorySessionStore()

    def respond(self, user_message: str, session_id: str | None = None) -> dict:
        """Process one customer message through the full agent pipeline."""
        session_id = session_id or str(uuid.uuid4())[:8]
        memory = self._session_store.get_or_create(
            session_id, metadata={"customer_email": self.customer_email}
        )

        # ── Pre-check: escalation triggers ───────────────────────────────────
        if self._check_escalation_triggers(user_message):
            memory.add_user_message(user_message)
            escalation_msg = (
                "I understand this is important to you. I'm immediately connecting you "
                "with a senior specialist who will prioritise your case."
            )
            memory.add_assistant_message(escalation_msg)
            return {
                "response": escalation_msg,
                "action": "escalate",
                "session_id": session_id,
                "intent": "escalate",
            }

        # ── Routing ───────────────────────────────────────────────────────────
        intent_result = self._classifier.classify(user_message, memory.messages)
        logger.info("intent_routed", intent=intent_result.intent, confidence=intent_result.confidence)

        memory.remember("last_intent", intent_result.intent)
        memory.add_user_message(user_message)

        # ── Tool use + response generation ───────────────────────────────────
        system_prompt = SPECIALIST_PROMPTS.get(intent_result.intent, SPECIALIST_PROMPTS["general"])
        messages = memory.get_messages_for_model(system_prompt)
        tool_calls_made: list[str] = []
        final_content = ""

        MAX_ITERATIONS = 8
        for iteration in range(MAX_ITERATIONS):
            try:
                response = self._executor.complete(
                    messages=messages,
                    tools=SUPPORT_TOOLS,
                    max_tokens=400,
                    temperature=0.0,
                )
            except Exception as exc:
                logger.error("executor_failed", error=str(exc))
                return self._service_error_response(session_id, intent_result.intent)

            if not response.tool_calls:
                final_content = response.content
                break

            messages.append(Message(
                role="assistant", content=response.content or "",
                tool_calls=response.tool_calls,
            ))

            for tc in response.tool_calls:
                tool_name = tc["function"]["name"]
                tool_args = json.loads(tc["function"]["arguments"])
                tool_result = self._execute_tool_safe(tool_name, tool_args, memory)
                tool_calls_made.append(tool_name)

                messages.append(Message(
                    role="tool", content=json.dumps(tool_result),
                    tool_call_id=tc["id"],
                ))

        # ── Guardrail check ───────────────────────────────────────────────────
        account_ctx = self._get_account_context(memory)
        guardrail_result = self._guardrails.check(final_content, account_ctx)

        if not guardrail_result.passed:
            if guardrail_result.has_critical:
                final_content = "I'm connecting you with a specialist to assist further."
                action = "escalate"
            else:
                final_content = self._regenerate_response(messages, guardrail_result)
                action = "continue"
        else:
            action = "continue"

        memory.add_assistant_message(final_content)
        self._session_store.save(memory)

        return {
            "response": final_content,
            "action": action,
            "session_id": session_id,
            "intent": intent_result.intent,
            "tool_calls": tool_calls_made,
        }

    def _execute_tool_safe(self, name: str, args: dict, memory: ConversationMemory) -> dict:
        func = TOOL_FUNCTIONS.get(name)
        if not func:
            return {"error": f"Unknown tool: {name}"}
        try:
            # Auto-inject customer_email where the tool requires it
            if "customer_email" in func.__code__.co_varnames and "customer_email" not in args:
                args["customer_email"] = self.customer_email
            result = func(**args)
            # Cache account info in memory for guardrail context
            if name == "get_customer_account" and result.get("found"):
                memory.remember("customer_tier", result.get("tier", "standard"))
                memory.remember("refunds_this_year", result.get("refunds_this_year", 0))
            return result
        except Exception as exc:
            logger.error("tool_failed", tool=name, error=str(exc))
            return {"error": "service_unavailable", "tool": name, "message": str(exc)}

    def _get_account_context(self, memory: ConversationMemory) -> dict:
        return {
            "customer_tier": memory.recall("customer_tier", "standard"),
            "refunds_this_year": memory.recall("refunds_this_year", 0),
        }

    def _check_escalation_triggers(self, message: str) -> bool:
        msg_lower = message.lower()
        return any(t in msg_lower for t in ESCALATION_TRIGGERS)

    def _regenerate_response(self, messages: list[Message], guardrail_result) -> str:
        constraint_msg = (
            f"Issue with previous response: {guardrail_result.summary}. "
            "Please rewrite — be helpful but avoid unauthorised promises."
        )
        try:
            regen = self._executor.complete(
                messages=messages + [Message(role="user", content=constraint_msg)],
                max_tokens=300,
            )
            return regen.content
        except Exception:
            return "Let me connect you with a specialist who can assist further."

    def _service_error_response(self, session_id: str, intent: str) -> dict:
        return {
            "response": "I'm experiencing a brief technical issue. A specialist will follow up shortly.",
            "action": "escalate",
            "session_id": session_id,
            "intent": intent,
        }


if __name__ == "__main__":
    print("🤖 Production Support Agent Demo\n")
    agent = ProductionSupportAgent(customer_email="jane@example.com")
    session_id = str(uuid.uuid4())[:8]

    conversation = [
        "Hi, my order 12345 hasn't arrived yet.",
        "When exactly will it be delivered?",
        "What's your return policy if it arrives damaged?",
    ]

    for msg in conversation:
        print(f"User: {msg}")
        try:
            result = agent.respond(msg, session_id=session_id)
            print(f"Intent: {result['intent']}")
            if result.get("tool_calls"):
                print(f"Tools used: {', '.join(result['tool_calls'])}")
            print(f"Agent: {result['response']}")
            print(f"Action: {result['action']}\n")

            if result["action"] == "escalate":
                print("→ Escalated to human agent")
                break
        except Exception as exc:
            print(f"Error: {exc}")
            print("Tip: Configure API keys in .env")
            break
