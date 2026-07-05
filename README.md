<div align="center">

# 🤖 Agentic Design Patterns
### Official Companion Repository

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![CI](https://github.com/your-org/agentic-design-patterns/workflows/CI/badge.svg)](https://github.com/your-org/agentic-design-patterns/actions)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

*The official companion repository for*
***Agentic Design Patterns: The Upgraded Companion***
*— June 2026*

</div>

---

## What This Repository Is

Every code example from the book, implemented as **production-quality, runnable Python**.

The book removed code to stay readable. This repository puts it all back — better engineered, fully tested, ready to deploy.

```bash
git clone https://github.com/your-org/agentic-design-patterns
cd agentic-design-patterns
pip install -r requirements-dev.txt && pip install -e .
cp .env.example .env          # Add your API key
pytest tests/unit/            # ✅ All tests pass (no API key needed)
python chapters/01-prompt-chaining/minimal/main.py
```

---

## Repository Structure

```
agentic-design-patterns/
├── src/agentic_patterns/          # Shared framework
│   ├── llm/providers/             # OpenAI, Anthropic, Google, Ollama, OpenRouter
│   ├── routing/                   # Intent classification
│   ├── memory/                    # Conversation memory + session store
│   ├── guardrails/                # Safety + business rule checker
│   ├── evaluation/                # LLM-as-Judge (pass@k, pass^k)
│   ├── telemetry/                 # Prometheus metrics + cost tracking
│   ├── workflow/                  # Core agent loop
│   └── utils/                    # Config, logging, cache, monitoring
│
├── chapters/                      # Pattern implementations
│   ├── 01-prompt-chaining/
│   ├── 02-routing/
│   ├── 03-model-selection/
│   ├── 04-tool-calling/
│   ├── 05-memory/
│   ├── 06-rag/
│   ├── 07-reflection/
│   ├── 08-guardrails/
│   ├── 09-human-approval/
│   ├── 10-workflows/
│   ├── 11-multi-agent/
│   └── 12-production-agent/       # All patterns combined
│
├── tests/
│   ├── unit/                      # Fast, no API key required
│   ├── integration/               # Require API keys
│   └── mocks/                     # MockProvider for offline testing
│
├── playground/app.py              # Streamlit interactive UI
├── benchmarks/                    # Cost, latency, accuracy measurement
├── examples/                      # Complete application examples
└── docker-compose.yml             # docker compose up → everything running
```

---

## Quick Start by Pattern

| Chapter | Pattern | Book Reference | Run |
|---------|---------|----------------|-----|
| 01 | Prompt Chaining | Gap 1: Model Landscape | `python chapters/01-prompt-chaining/minimal/main.py` |
| 02 | Routing | Gap 2: Framework Bias | `python chapters/02-routing/minimal/main.py` |
| 04 | Tool Calling | Gap 3: Isolation Problem | `python chapters/04-tool-calling/minimal/main.py` |
| 08 | Guardrails | Gap 4: Safety Blindspot | `python chapters/08-guardrails/minimal/main.py` |
| 12 | Production Agent | Gap 3: All patterns combined | `python chapters/12-production-agent/production/main.py` |

---

## Multi-Provider Support

Every example works with any supported provider — swap with one environment variable:

```bash
# OpenAI (default)
DEFAULT_PROVIDER=openai EXECUTOR_MODEL=gpt-4.1 python chapters/12-production-agent/production/main.py

# Anthropic
DEFAULT_PROVIDER=anthropic EXECUTOR_MODEL=claude-sonnet-4-6 python ...

# Google
DEFAULT_PROVIDER=google EXECUTOR_MODEL=gemini-2.5-flash python ...

# Local (Ollama — no API key needed)
DEFAULT_PROVIDER=ollama EXECUTOR_MODEL=qwen3:14b python ...
```

---

## Docker

```bash
docker compose up          # Starts: app + Streamlit playground + ChromaDB + Prometheus + Grafana
```

Services:
| Service | URL | Purpose |
|---------|-----|---------|
| Playground | http://localhost:8501 | Interactive pattern explorer |
| Prometheus | http://localhost:9090 | Metrics |
| Grafana | http://localhost:3000 | Dashboards (admin/admin) |
| ChromaDB | http://localhost:8000 | Vector store |

---

## Running Tests

```bash
# Unit tests — no API keys required, runs in seconds
pytest tests/unit/ -v

# Chapter tests — no API keys required
pytest chapters/ -v

# Full suite with coverage (requires API keys)
pytest --cov=src --cov-report=html

# Cost benchmark (no API keys — uses mock pricing)
python benchmarks/cost_benchmark.py
```

---

## Providers Supported

| Provider | Models | Requires |
|----------|--------|----------|
| OpenAI | GPT-4.1 Nano/Mini/Full, GPT-5.4/5.5, o4-mini, o3 | `OPENAI_API_KEY` |
| Anthropic | Claude Haiku 4.5, Sonnet 4.6, Opus 4.6/4.7/4.8, Fable 5 | `ANTHROPIC_API_KEY` |
| Google | Gemini 2.5 Flash-Lite/Flash, 3.5 Flash, 3.1 Pro | `GOOGLE_API_KEY` |
| Azure OpenAI | Any Azure deployment | `AZURE_OPENAI_API_KEY` |
| OpenRouter | Any model via OpenRouter | `OPENROUTER_API_KEY` |
| Ollama | DeepSeek V4, Qwen 3, Llama 4, Gemma 4, Mistral | Local — no key needed |

---

## Book References

This repository implements every code example from the book, organised by gap:

| Book Chapter | Pattern(s) | Repository Location |
|-------------|-----------|---------------------|
| Gap 1: Model Landscape | Model cascade, context windows, reasoning models | `src/agentic_patterns/llm/providers/factory.py` |
| Gap 2: Framework Bias | Provider abstraction | `src/agentic_patterns/llm/providers/` |
| Gap 3: Isolation Problem | Combined agent, all 6 patterns | `chapters/12-production-agent/` |
| Gap 4: Safety Blindspot | Guardrails, injection detection, tool privilege | `src/agentic_patterns/guardrails/` |
| Gap 5: Cost & Latency | Cost calculator, caching, latency budgets | `src/agentic_patterns/telemetry/`, `benchmarks/` |
| Gap 6: Harness Engineering | LLM judge, pass@k, CI/CD | `src/agentic_patterns/evaluation/` |
| Gap 7: Databricks | Data-platform-native agents | `examples/databricks-agent/` |
| Gap 8: A2A Protocol | Agent-to-agent communication | `chapters/11-multi-agent/` |
| Ch 9: Proprietary Models | OpenAI, Anthropic, Google pricing | `src/agentic_patterns/llm/providers/` |
| Ch 10: Open-Source Models | Ollama, DeepSeek, Qwen, Llama | `src/agentic_patterns/llm/providers/ollama_provider.py` |

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). All contributions welcome.

**The quality target:**
> If O'Reilly, Microsoft, Google DeepMind, Anthropic, and OpenAI collaborated on an educational open-source repository, this should be comparable in engineering quality.

---

<div align="center">

MIT License · June 2026 · Built with ❤️ for the agentic AI community

</div>
