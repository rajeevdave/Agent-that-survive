# Model Selection Guide (June 2026)

## The Core Principle

**Use the cheapest model that reliably handles each task.**

The factory provides three pre-configured tiers:

```python
from agentic_patterns.llm.providers.factory import (
    create_router_provider,    # Cheapest — for routing/classification
    create_executor_provider,  # Mid-tier — for most agent tasks
    create_reasoner_provider,  # Reasoning model — for planning/reflection
)
```

Configure via environment variables:
```bash
ROUTER_MODEL=gpt-4.1-nano       # $0.10/M — classification, routing
EXECUTOR_MODEL=gpt-4.1          # $2.00/M — tool use, synthesis
REASONER_MODEL=o4-mini          # $0.55/M — planning, complex reasoning
```

## June 2026 Pricing Quick Reference

| Model | Input $/M | Output $/M | Best for |
|-------|-----------|------------|---------|
| GPT-4.1 Nano | $0.10 | $0.40 | Routing, classification |
| Gemini 2.5 Flash-Lite | $0.10 | $0.40 | Budget routing |
| Claude Haiku 4.5 | $1.00 | $5.00 | Triage, extraction |
| GPT-4.1 | $2.00 | $8.00 | Production workhorse |
| Claude Sonnet 4.6 | $3.00 | $15.00 | Most agentic tasks |
| o4-mini | $0.55 | $2.20 | Budget reasoning |
| Claude Opus 4.8 | $5.00 | $25.00 | Complex, long-horizon |
| GPT-5.5 | $5.00 | $30.00 | Frontier capability |

## Open-Source Models (via Ollama — Free)

```bash
ollama pull qwen3:14b          # Best local all-rounder
ollama pull deepseek-v4-flash  # MIT license, 1M context
ollama pull llama4:scout       # 10M context, single H100
ollama pull gemma4:26b         # 14GB VRAM, 85 tok/s
```

## Migration from Original Book Models

| Old (book) | New (June 2026) | Why |
|------------|-----------------|-----|
| `gemini-2.0-flash-exp` | `gemini-2.5-flash-lite` | **BROKEN** — shut down June 1 2026 |
| `gpt-4o` | `gpt-4.1` | 8× context, cheaper, better |
| `claude-3-5-sonnet` | `claude-sonnet-4-6` | Same price, significantly better |
| `claude-3-opus` | `claude-opus-4-8` | 67% cheaper, better capability |

## Decision Flowchart

```
Is this routing/classification? → Use ROUTER_MODEL (cheapest)
  ↓ No
Does it need long-horizon planning or math? → Use REASONER_MODEL (o4-mini/o3)
  ↓ No
Does context exceed 200K tokens? → Use Gemini 3.1 Pro (2M context)
  ↓ No
Standard production task → Use EXECUTOR_MODEL (GPT-4.1 / Sonnet 4.6)
```
