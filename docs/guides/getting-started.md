# Getting Started

## Prerequisites

- Python 3.11+
- At least one LLM provider API key (or Ollama running locally — no key needed)

## Installation

```bash
# Clone the repository
git clone https://github.com/rajeevdave/Agent-that-survive.git
cd Agent-that-survive

# Create virtual environment
python -m venv .venv
source .venv/bin/activate          # Linux/Mac
# .venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements-dev.txt
pip install -e .

# Configure environment
cp .env.example .env
# Edit .env and add your API key(s)
```

## Verify Installation

```bash
# Run unit tests — no API keys required
pytest tests/unit/ -v

# Check structure
python scripts/verify_structure.py

# Run the cost benchmark (no API keys needed)
python benchmarks/cost_benchmark.py
```

## Your First Agent

```python
from agentic_patterns.llm.providers.factory import create_provider
from agentic_patterns.llm.providers.base import Message
from agentic_patterns.workflow.agent_loop import AgentLoop
from agentic_patterns.memory.conversation_memory import ConversationMemory

# Create provider (reads from .env automatically)
llm = create_provider()

# Create agent loop with guardrails built in
agent = AgentLoop(provider=llm, system_prompt="You are a helpful assistant.")

# Run a conversation
memory = ConversationMemory(session_id="demo")
result = agent.run("What is the capital of France?", memory=memory)
print(result.content)   # "The capital of France is Paris."
```

## Using Different Providers

```bash
# OpenAI (default)
DEFAULT_PROVIDER=openai EXECUTOR_MODEL=gpt-4.1 python examples/customer-support/main.py

# Anthropic
DEFAULT_PROVIDER=anthropic EXECUTOR_MODEL=claude-sonnet-4-6 python ...

# Google
DEFAULT_PROVIDER=google EXECUTOR_MODEL=gemini-2.5-flash python ...

# Local — no API key needed (requires: ollama pull qwen3:14b)
DEFAULT_PROVIDER=ollama EXECUTOR_MODEL=qwen3:14b python ...
```

## Run the Playground

```bash
# Install Streamlit
pip install streamlit

# Start the interactive playground
streamlit run playground/app.py
# Opens at http://localhost:8501
```

## Docker

```bash
# Start everything: app + playground + ChromaDB + Prometheus + Grafana
docker compose up

# Services:
# Playground:  http://localhost:8501
# Prometheus:  http://localhost:9090
# Grafana:     http://localhost:3000  (admin/admin)
# ChromaDB:    http://localhost:8000
```
