"""Mock LLM provider for unit testing without API keys."""
from typing import Any, Optional
from agentic_patterns.llm.providers.base import Message, LLMResponse


class MockProvider:
    def __init__(
        self,
        responses: Optional[list[str]] = None,
        default_response: str = "Mock response",
        tool_calls_sequence: Optional[list[Optional[list[dict[str, Any]]]]] = None,
    ):
        self.responses = responses or []
        self.default_response = default_response
        self.tool_calls_sequence = tool_calls_sequence or []
        self._call_index = 0
        self.calls: list[list[Message]] = []

    def complete(self, messages: list[Message], **kwargs: Any) -> LLMResponse:
        self.calls.append(messages)
        if self._call_index < len(self.responses):
            resp_content = self.responses[self._call_index]
        else:
            resp_content = self.default_response

        tool_calls = None
        if self._call_index < len(self.tool_calls_sequence):
            tool_calls = self.tool_calls_sequence[self._call_index]

        self._call_index += 1
        return LLMResponse(content=resp_content, tool_calls=tool_calls)

    def generate(self, prompt: str, **kwargs: Any) -> str:
        res = self.complete([Message(role="user", content=prompt)], **kwargs)
        return res.content
