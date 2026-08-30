# Chapter XX: Pattern Name

## Problem

*What problem does this pattern solve? Why does it exist?*

## Architecture

*High-level diagram showing how this pattern works.*

```
Input → [Step 1] → [Step 2] → Output
```

## When to Use

- **Use this pattern when:** ...
- **Skip this pattern when:** ...

## Minimal Example

See `minimal/main.py` — run with:
```bash
python book-code/XX-pattern-name/minimal/main.py
```

## Production Example

See `production/main.py` — includes logging, retries, cost tracking.

## Book Reference

*Which gap or chapter in the book introduces this pattern.*

## Trade-offs

| Dimension | Value | Notes |
|-----------|-------|-------|
| Latency | +N ms | Adds N ms per LLM call |
| Cost | +$X/1k queries | At default model tier |
| Complexity | Low/Medium/High | |

## Common Mistakes

1. **Using frontier model for routing** — Use the cheapest model that classifies accurately.
2. ...

## Further Reading

- Book: Chapter X, Gap Y
- `src/agentic_patterns/module_name/`
- Related patterns: Pattern A, Pattern B
