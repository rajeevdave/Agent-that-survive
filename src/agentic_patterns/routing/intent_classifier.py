"""Intent classification module for routing pattern."""
from dataclasses import dataclass
from typing import Any, Optional
from agentic_patterns.llm.providers.base import LLMProvider, Message


@dataclass
class IntentResult:
    intent: str
    confidence: float = 0.95
    reasoning: str = ""


class IntentClassifier:
    def __init__(
        self,
        provider: Optional[LLMProvider] = None,
        llm: Optional[LLMProvider] = None,
        routes: Optional[list[str]] = None,
        intents: Optional[list[str]] = None,
        intent_descriptions: Optional[dict[str, str]] = None,
        default_intent: str = "general",
    ):
        self.llm = provider or llm
        self.intents = intents or routes or ["general"]
        self.default_intent = default_intent

    def classify(
        self,
        user_input: str,
        messages: Optional[list[Message]] = None,
        conversation_history: Optional[list[Message]] = None,
    ) -> IntentResult:
        hist = conversation_history or messages or []
        hist_text = "\n".join([f"{m.role}: {m.content}" for m in hist])
        prompt = f"History:\n{hist_text}\nClassify input into one of {self.intents}: {user_input}"

        if self.llm:
            try:
                resp = self.llm.complete([Message(role="user", content=prompt)])
                content = resp.content.strip()

                if content.startswith("{") and content.endswith("}"):
                    import json
                    data = json.loads(content)
                    intent = data.get("intent", self.default_intent)
                    if intent not in self.intents:
                        intent = self.default_intent
                    return IntentResult(
                        intent=intent,
                        confidence=float(data.get("confidence", 0.0)),
                        reasoning=data.get("reasoning", ""),
                    )

                for r in self.intents:
                    if r.lower() in content.lower():
                        return IntentResult(intent=r, confidence=0.9)
            except Exception:
                pass

        return IntentResult(intent=self.default_intent, confidence=0.0)
