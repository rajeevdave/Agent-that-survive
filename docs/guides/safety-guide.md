# Safety Guide

## The Core Principle

Safety is an architectural constraint, not a chapter you add at the end.
Every pattern needs its own safety analysis.

## Guardrail Checker

```python
from agentic_patterns.guardrails.checker import GuardrailChecker

checker = GuardrailChecker()
result = checker.check(response_text, context={"customer_tier": "premium"})

if not result.passed:
    if result.has_critical:
        # Escalate to human immediately
    else:
        # Regenerate with constraint
```

## Prompt Injection Prevention

```python
from agentic_patterns.guardrails.checker import InjectionSanitiser

sanitiser = InjectionSanitiser()
risk = sanitiser.assess_risk(external_content)  # "low" | "medium" | "high"
safe_content = sanitiser.wrap_external_content(external_content, "WEB PAGE")
# Now safe to include in agent context
```

## RAG Trust Levels

```python
from agentic_patterns.rag.retrieval.retriever import Document, TrustLevel

# Always label documents with their trust level
doc = Document("id", content, trust_level=TrustLevel.USER_SUBMITTED)

# Retriever automatically filters by trust
retriever = InMemoryRetriever(max_trust_score=2)  # Only admin/internal/reviewed
```

## HITL for Irreversible Actions

```python
from agentic_patterns.approval.hitl import HITLGate, ReversibilityClass, ApprovalRequest
import uuid

gate = HITLGate(approval_fn=my_approval_fn)

request = ApprovalRequest(
    request_id=str(uuid.uuid4()),
    action="send_email",
    parameters={"to": "customer@example.com", "subject": "..."},
    reversibility=ReversibilityClass.IRREVERSIBLE,
    requester="support_agent",
)

if gate.requires_approval(request.reversibility):
    approved = gate.request_approval(request)
    if not approved:
        return  # User rejected
```

## Attack Surface Checklist

Run this mental checklist before deploying any agent:

- [ ] All user input sanitised before adding to context
- [ ] All external content (web, DB, docs) wrapped with InjectionSanitiser
- [ ] All tools have minimum required permissions
- [ ] All irreversible tools gated with HITL
- [ ] Guardrails run on every response before delivery
- [ ] Multi-agent: sub-agent outputs treated as untrusted data
- [ ] RAG: documents labelled with trust levels
- [ ] Audit logging enabled for all tool calls
