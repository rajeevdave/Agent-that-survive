# Contributing to Agentic Design Patterns

Thank you for helping make this the best agentic AI resource available.

## Quick Start

```bash
git clone https://github.com/your-org/agentic-design-patterns.git
cd agentic-design-patterns
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
pip install -e .
cp .env.example .env  # Add your API keys
pytest tests/unit/    # Run tests (no API keys needed)
```

## Repository Structure

```
src/agentic_patterns/    # Shared framework — all reusable modules
chapters/XX-name/        # One directory per pattern
  minimal/               # Simplest working implementation
  production/            # Production-grade implementation
  tests/                 # Chapter-specific tests
tests/                   # Framework-level tests
  unit/                  # Fast, no API calls
  integration/           # Require API keys
  mocks/                 # Shared mock providers
playground/              # Streamlit interactive UI
benchmarks/              # Cost, latency, accuracy measurement
examples/                # Complete application examples
```

## Adding a New Chapter

1. Copy `chapters/01-prompt-chaining/` as your template
2. Implement `minimal/main.py` — simplest possible working example
3. Implement `production/main.py` — production-quality with logging, retries, metrics
4. Write tests in `tests/` — all tests must run with `MockProvider` (no real API calls)
5. Write `README.md` using the template in `docs/guides/chapter-readme-template.md`
6. Add diagrams in `mermaid.md` and `architecture.md`
7. Open a PR — CI must pass before merge

## Engineering Standards

- **Type hints**: all function signatures must have complete type annotations
- **Docstrings**: every public function/class needs a docstring with book reference
- **No TODOs**: every function must be complete and runnable
- **Tests first**: write tests before implementation where possible
- **Mock tests**: chapter tests must not require API keys to run
- **Logging**: use `get_logger(__name__)` from `agentic_patterns.utils.logging`
- **Configuration**: no hardcoded strings — use `settings` from configuration module

## Commit Message Format

```
feat(chapter-01): add parallel execution variant
fix(routing): handle empty conversation history
docs(readme): update model pricing table for June 2026
test(guardrails): add edge case for empty response
```

## Pull Request Checklist

- [ ] All tests pass: `pytest tests/unit/`
- [ ] Linting passes: `ruff check src/ chapters/ tests/`
- [ ] Type checking: `mypy src/agentic_patterns/`
- [ ] No hardcoded API keys or secrets
- [ ] Book reference in every module docstring
- [ ] README updated if adding new chapter
