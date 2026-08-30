"""Base interface and dataclasses for LLM providers."""
from dataclasses import dataclass, field
from typing import Any, Optional, Protocol, Union


@dataclass
class ToolDefinition:
    name: str
    description: str
    parameters: dict[str, Any]


@dataclass
class Message:
    role: str
    content: str
    name: Optional[str] = None
    tool_calls: Optional[list[dict[str, Any]]] = None
    tool_call_id: Optional[str] = None


@dataclass
class LLMResponse:
    content: str = ""
    model: str = "mock-model"
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    tool_calls: Optional[list[dict[str, Any]]] = None
    raw: Optional[Any] = None


class LLMProvider(Protocol):
    def complete(self, messages: list[Message], **kwargs: Any) -> LLMResponse:
        ...
