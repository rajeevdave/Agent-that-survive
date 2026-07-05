"""
Chapter 1: Prompt Chaining — Minimal Example

Demonstrates the simplest form of prompt chaining:
a linear sequence where each step's output feeds the next.

Book reference: Gap 1 (Model Landscape) — Prompt Chaining remains fully relevant
regardless of model generation. Individual steps can be more ambitious with
reasoning models, but the chain structure itself is unchanged.

Run:
    python chapters/01-prompt-chaining/minimal/main.py
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../src"))

from agentic_patterns.llm.providers.base import Message
from agentic_patterns.llm.providers.factory import create_provider
from agentic_patterns.utils.logging.logger import get_logger

logger = get_logger(__name__)


def run_prompt_chain(topic: str) -> dict[str, str]:
    """
    Three-step prompt chain:
    1. Research: generate key facts about the topic
    2. Outline: structure those facts into a report outline
    3. Draft: write a concise report from the outline

    Each step's output becomes the next step's input.
    """
    llm = create_provider()
    results: dict[str, str] = {}

    # Step 1: Research
    logger.info("chain_step_1", step="research", topic=topic)
    research_response = llm.complete(
        messages=[
            Message(
                role="system",
                content="You are a research assistant. Be factual and concise.",
            ),
            Message(
                role="user",
                content=f"List 5 key facts about: {topic}. Be specific and accurate.",
            ),
        ],
        max_tokens=500,
    )
    results["research"] = research_response.content
    logger.info("step_1_complete", tokens=research_response.total_tokens)

    # Step 2: Outline — uses step 1 output
    logger.info("chain_step_2", step="outline")
    outline_response = llm.complete(
        messages=[
            Message(
                role="system",
                content="You are a technical writer. Create clear, logical outlines.",
            ),
            Message(
                role="user",
                content=(
                    f"Using these research facts:\n{results['research']}\n\n"
                    "Create a structured 3-section outline for a short report."
                ),
            ),
        ],
        max_tokens=400,
    )
    results["outline"] = outline_response.content
    logger.info("step_2_complete", tokens=outline_response.total_tokens)

    # Step 3: Draft — uses step 2 output
    logger.info("chain_step_3", step="draft")
    draft_response = llm.complete(
        messages=[
            Message(
                role="system",
                content="You are a professional writer. Write clear, engaging content.",
            ),
            Message(
                role="user",
                content=(
                    f"Write a concise 200-word report using this outline:\n{results['outline']}"
                ),
            ),
        ],
        max_tokens=600,
    )
    results["draft"] = draft_response.content
    logger.info("step_3_complete", tokens=draft_response.total_tokens)

    return results


if __name__ == "__main__":
    topic = sys.argv[1] if len(sys.argv) > 1 else "agentic AI systems"
    print(f"\n🔗 Running prompt chain for: '{topic}'\n")

    try:
        results = run_prompt_chain(topic)
        print("── RESEARCH FACTS ──────────────────────")
        print(results["research"])
        print("\n── OUTLINE ─────────────────────────────")
        print(results["outline"])
        print("\n── FINAL REPORT ────────────────────────")
        print(results["draft"])
    except Exception as exc:
        print(f"Error: {exc}")
        print("Tip: Set OPENAI_API_KEY or configure another provider in .env")
        sys.exit(1)
