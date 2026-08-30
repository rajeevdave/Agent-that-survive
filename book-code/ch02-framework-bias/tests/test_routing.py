"""Tests for Chapter 2: Routing."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../src"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../tests"))

import pytest
from mocks.mock_provider import MockProvider
from agentic_patterns.routing.intent_classifier import IntentClassifier
from agentic_patterns.memory.conversation_memory import ConversationMemory
from agentic_patterns.llm.providers.base import Message

INTENTS = ["billing", "order_status", "returns", "general"]


class TestIntentClassifier:
    def test_classifies_known_intent(self):
        mock = MockProvider(responses=['{"intent": "billing", "confidence": 0.9, "reasoning": "invoice"}'])
        classifier = IntentClassifier(provider=mock, intents=INTENTS)
        result = classifier.classify("My invoice is wrong")
        assert result.intent == "billing"
        assert result.confidence == 0.9

    def test_falls_back_to_default_on_bad_json(self):
        mock = MockProvider(responses=["not valid json"])
        classifier = IntentClassifier(
            provider=mock, intents=INTENTS, default_intent="general"
        )
        result = classifier.classify("something")
        assert result.intent == "general"
        assert result.confidence == 0.0

    def test_falls_back_on_unknown_intent(self):
        mock = MockProvider(responses=['{"intent": "nonexistent", "confidence": 0.5}'])
        classifier = IntentClassifier(
            provider=mock, intents=INTENTS, default_intent="general"
        )
        result = classifier.classify("anything")
        assert result.intent == "general"

    def test_includes_conversation_history(self):
        """Classifier passes history to help classify follow-up messages."""
        received_prompts = []
        class CapturingMock(MockProvider):
            def complete(self, messages, **kwargs):
                received_prompts.append(messages[0].content)
                return super().complete(messages, **kwargs)

        mock = CapturingMock(responses=['{"intent": "order_status", "confidence": 0.8}'])
        classifier = IntentClassifier(provider=mock, intents=INTENTS)
        history = [Message(role="user", content="My order is late")]
        classifier.classify("Can I get an update?", conversation_history=history)
        assert "Can I get an update?" in received_prompts[0]
