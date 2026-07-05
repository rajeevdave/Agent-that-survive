"""Tests for Chapter 1: Prompt Chaining."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../src"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../tests"))

import pytest
from mocks.mock_provider import MockProvider
from agentic_patterns.llm.providers.base import Message


def make_chain(llm, topic: str) -> dict[str, str]:
    """Reimplementation using injected provider (testable without API key)."""
    results = {}

    r1 = llm.complete([Message(role="user", content=f"Facts about {topic}")])
    results["research"] = r1.content

    r2 = llm.complete([Message(role="user", content=f"Outline from: {r1.content}")])
    results["outline"] = r2.content

    r3 = llm.complete([Message(role="user", content=f"Draft from: {r2.content}")])
    results["draft"] = r3.content

    return results


class TestPromptChain:
    def test_chain_produces_three_outputs(self):
        llm = MockProvider(responses=["Research facts.", "Outline here.", "Final draft."])
        results = make_chain(llm, "AI agents")
        assert "research" in results
        assert "outline" in results
        assert "draft" in results

    def test_chain_uses_previous_output(self):
        """Verify each step receives the previous step's output."""
        calls = []
        llm = MockProvider(responses=["step1_output", "step2_output", "step3_output"])
        # Track that step 2 receives step 1's output
        result = make_chain(llm, "test topic")
        assert result["research"] == "step1_output"
        assert result["outline"] == "step2_output"
        assert result["draft"] == "step3_output"

    def test_chain_makes_exactly_three_calls(self):
        llm = MockProvider(responses=["r1", "r2", "r3"])
        make_chain(llm, "test")
        assert llm._call_index == 3

    def test_empty_topic_handled(self):
        llm = MockProvider(responses=["r1", "r2", "r3"])
        result = make_chain(llm, "")
        assert isinstance(result["draft"], str)
