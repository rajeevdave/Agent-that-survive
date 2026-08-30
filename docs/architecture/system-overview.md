# System Architecture

## Layer Model

```
┌─────────────────────────────────────────────────────────┐
│                    Application Layer                      │
│         examples/ • playground/ • book-code/               │
├─────────────────────────────────────────────────────────┤
│                   Pattern Layer                           │
│  Routing • Memory • Tools • Reflection • Planning        │
│  Guardrails • HITL • RAG • Evaluation • Multi-Agent      │
├─────────────────────────────────────────────────────────┤
│               Provider Abstraction Layer                  │
│  OpenAI • Anthropic • Google • Ollama • OpenRouter       │
├─────────────────────────────────────────────────────────┤
│                Infrastructure Layer                       │
│  Logging • Metrics • Cache • Config • Telemetry          │
└─────────────────────────────────────────────────────────┘
```

## Provider Abstraction (Gap 2 — Framework Bias)

All agent code depends on `BaseLLMProvider`, never on vendor SDKs:

```
BaseLLMProvider (abstract)
├── OpenAIProvider      (GPT-4.1, GPT-5.x, o4-mini, o3)
├── AnthropicProvider   (Claude Haiku/Sonnet/Opus/Fable)
├── GoogleProvider      (Gemini 2.5/3.x Flash, 3.1 Pro)
├── OllamaProvider      (DeepSeek, Qwen, Llama 4, Gemma 4, Mistral)
└── (add your own by subclassing)
```

## Agent Loop (Gap 3 — Isolation Problem)

```
User Message
    │
    ▼
[Escalation Check] ──yes──► Human Agent
    │ no
    ▼
[Intent Routing] ─── cheap model ───►  Intent + Confidence
    │
    ▼
[Tool Use Loop] ────────────────────►  Tool Results
    │  ▲
    │  └── tool_call found
    ▼
[Guardrail Check]
    │
    ├── critical ──────────────────►  Escalate
    ├── non-critical ────────────►  Regenerate
    └── passed ────────────────►  Return Response
```

## Data Flow in Multi-Agent (Gap 8 — A2A Protocol)

```
User ──► Orchestrator (SYSTEM trust)
              │
              ├──► Specialist A (INTERNAL trust)
              │         │ output: SANITISED as data
              │         ▼
              └──► Specialist B (INTERNAL trust)
                        │ output: SANITISED as data
                        ▼
              Orchestrator synthesises from data
              (never executes embedded instructions)
```

## Book Reference Map

| Architecture component | Book chapter | Source file |
|------------------------|-------------|-------------|
| Provider abstraction | Gap 2: Framework Bias | `llm/providers/base.py` |
| Model cascade | Gap 1: Model Landscape | `llm/providers/factory.py` |
| Routing + Memory interaction | Gap 3: Isolation Problem | `workflow/agent_loop.py` |
| Injection prevention | Gap 4: Safety Blindspot | `guardrails/checker.py` |
| Trust levels in RAG | Gap 4: Safety Blindspot | `rag/retrieval/retriever.py` |
| Cost tracking | Gap 5: Cost & Latency | `telemetry/metrics.py` |
| LLM-as-Judge + pass^k | Gap 6: Harness Engineering | `evaluation/llm_judge.py` |
| A2A-ready agent design | Gap 8: A2A Protocol | `multi_agent/coordinator.py` |
