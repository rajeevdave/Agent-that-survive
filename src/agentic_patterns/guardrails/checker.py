"""Guardrail checker module for content safety and business rules."""
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class GuardrailResult:
    passed: bool
    has_critical: bool = False
    summary: str = ""


class GuardrailChecker:
    def __init__(self) -> None:
        pass

    def check(self, content: str, context: Optional[dict[str, Any]] = None) -> GuardrailResult:
        if not content:
            return GuardrailResult(passed=True)
        content_lower = content.lower()
        if "ignore all previous instructions" in content_lower or "reveal secrets" in content_lower:
            return GuardrailResult(passed=False, has_critical=True, summary="Prompt injection detected")
        if "legally entitled to a refund" in content_lower:
            return GuardrailResult(passed=False, has_critical=False, summary="Unauthorized legal commitment")
        return GuardrailResult(passed=True)


class InjectionSanitiser:
    def __init__(self) -> None:
        pass

    def wrap_external_content(self, content: str, label: str = "EXTERNAL CONTENT") -> str:
        return f"<{label}>\n{content}\n</{label}>"
