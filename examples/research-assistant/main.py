"""
Example Application: Research Assistant

Uses Prompt Chaining + Reflection + RAG to research topics,
synthesise findings, and produce structured reports.

Run:
    python examples/research-assistant/main.py "agentic AI systems 2026"
"""
from __future__ import annotations
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../src"))

from agentic_patterns.llm.providers.base import Message
from agentic_patterns.llm.providers.factory import create_provider
from agentic_patterns.reflection.reflector import Reflector
from agentic_patterns.utils.logging.logger import get_logger

logger = get_logger(__name__)


def research_and_report(topic: str) -> dict[str, str]:
    """
    Three-stage research pipeline:
    1. Gather key facts (Prompt Chaining)
    2. Synthesise into structured report (Tool Use)
    3. Reflect and improve quality (Reflection)
    """
    llm = create_provider()
    results = {}

    # Stage 1: Research facts
    r1 = llm.complete([
        Message(role="system", content="You are a research expert. Be specific, factual, and cite relevant details."),
        Message(role="user", content=f"Research this topic thoroughly. List 8 key facts:\n\n{topic}"),
    ], max_tokens=800)
    results["facts"] = r1.content

    # Stage 2: Structure into report
    r2 = llm.complete([
        Message(role="system", content="You are a technical writer. Create clear, structured reports."),
        Message(role="user", content=f"Write a 300-word structured report on '{topic}' using:\n{results['facts']}"),
    ], max_tokens=600)
    results["draft"] = r2.content

    # Stage 3: Reflect and improve
    reflector = Reflector(generator=llm, max_iterations=2, quality_threshold=0.85)
    reflection_result = reflector.reflect(
        task=f"Write a high-quality research report on: {topic}",
        initial_output=results["draft"],
    )
    results["final_report"] = reflection_result.final_output
    results["iterations"] = str(reflection_result.iterations)

    return results


if __name__ == "__main__":
    topic = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "agentic AI systems in 2026"
    print(f"\n📚 Researching: {topic}\n")
    try:
        results = research_and_report(topic)
        print("=" * 60)
        print("FINAL REPORT")
        print("=" * 60)
        print(results["final_report"])
        print(f"\n[Improved in {results['iterations']} reflection iteration(s)]")
    except Exception as exc:
        print(f"Error: {exc}\nTip: Configure API keys in .env")
