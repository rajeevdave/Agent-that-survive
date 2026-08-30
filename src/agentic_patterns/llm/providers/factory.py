"""LLM provider factory for creating default providers and router providers."""
import os
from typing import Any
from agentic_patterns.llm.providers.base import LLMProvider, Message, LLMResponse


class DefaultProvider:
    def __init__(self, model: str = "gpt-4.1") -> None:
        self.model = model

    def complete(self, messages: list[Message], **kwargs: Any) -> LLMResponse:
        return LLMResponse(content="Default response", model=self.model)


def create_provider(provider_type: str = "default", **kwargs: Any) -> LLMProvider:
    return DefaultProvider(model=kwargs.get("model", "gpt-4.1"))


def create_router_provider(**kwargs: Any) -> LLMProvider:
    return DefaultProvider(model="router-model")
