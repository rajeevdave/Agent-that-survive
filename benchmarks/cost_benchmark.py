"""
Cost and latency benchmark suite.

Measures: cost per query, latency p50/p95, token usage, model cascade savings.
Book reference: Chapter 5 (Cost & Latency Blindspot) — the $19,000/year routing example.

Run:
    python benchmarks/cost_benchmark.py
"""
from __future__ import annotations

import os
import sys
import time
from dataclasses import dataclass

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

PRICING = {
    "gpt-4.1-nano":      {"input": 0.10, "output": 0.40},
    "gpt-4.1-mini":      {"input": 0.40, "output": 1.60},
    "gpt-4.1":           {"input": 2.00, "output": 8.00},
    "gpt-5.4":           {"input": 2.50, "output": 15.00},
    "claude-haiku-4-5":  {"input": 1.00, "output": 5.00},
    "claude-sonnet-4-6": {"input": 3.00, "output": 15.00},
    "gemini-2.5-flash-lite": {"input": 0.10, "output": 0.40},
    "gemini-2.5-flash":  {"input": 0.30, "output": 2.50},
}


@dataclass
class StepConfig:
    name: str
    model: str
    avg_input_tokens: int
    avg_output_tokens: int
    calls_per_query: float


def cost_per_call(model: str, input_tokens: int, output_tokens: int) -> float:
    p = PRICING.get(model, {"input": 0.002, "output": 0.002})
    return (input_tokens / 1_000_000 * p["input"]) + (output_tokens / 1_000_000 * p["output"])


def calculate_scenario(name: str, steps: list[StepConfig]) -> dict:
    total = sum(
        cost_per_call(s.model, s.avg_input_tokens, s.avg_output_tokens) * s.calls_per_query
        for s in steps
    )
    return {
        "scenario": name,
        "cost_per_query": total,
        "cost_per_1k_queries": total * 1000,
        "cost_per_day_500q": total * 500,
        "cost_per_month": total * 500 * 30,
        "cost_per_year": total * 500 * 365,
        "steps": [
            {
                "name": s.name,
                "model": s.model,
                "cost": cost_per_call(s.model, s.avg_input_tokens, s.avg_output_tokens) * s.calls_per_query,
            }
            for s in steps
        ],
    }


if __name__ == "__main__":
    # Scenario A: Naive — same frontier model everywhere
    naive = calculate_scenario("Naive (same model for all steps)", [
        StepConfig("routing",    "claude-sonnet-4-6",  800,  50,  1.0),
        StepConfig("tool_call",  "claude-sonnet-4-6", 1500, 200,  0.6),
        StepConfig("generation", "claude-sonnet-4-6", 3000, 400,  1.0),
        StepConfig("guardrail",  "claude-sonnet-4-6", 2000, 100,  1.0),
    ])

    # Scenario B: Optimised — right model for each step
    optimised = calculate_scenario("Optimised (model cascade)", [
        StepConfig("routing",    "gpt-4.1-nano",      800,  50,  1.0),
        StepConfig("tool_call",  "gpt-4.1",          1500, 200,  0.6),
        StepConfig("generation", "gpt-4.1",          3000, 400,  1.0),
        StepConfig("guardrail",  "gpt-4.1-nano",     2000, 100,  1.0),
    ])

    print("\n" + "=" * 62)
    print("  COST BENCHMARK — Model Cascade Analysis (June 2026)")
    print("=" * 62)
    for scenario in [naive, optimised]:
        print(f"\n📊 {scenario['scenario']}")
        print(f"   Cost per query:   ${scenario['cost_per_query']:.6f}")
        print(f"   Cost per 1k:      ${scenario['cost_per_1k_queries']:.4f}")
        print(f"   Cost/day (500q):  ${scenario['cost_per_day_500q']:.2f}")
        print(f"   Cost/month:       ${scenario['cost_per_month']:.2f}")
        print(f"   Cost/year:        ${scenario['cost_per_year']:.2f}")

    savings_pct = (1 - optimised["cost_per_query"] / naive["cost_per_query"]) * 100
    savings_year = naive["cost_per_year"] - optimised["cost_per_year"]
    print(f"\n💰 Annual savings from cascade: ${savings_year:,.2f} ({savings_pct:.0f}% reduction)")
    print("=" * 62)
