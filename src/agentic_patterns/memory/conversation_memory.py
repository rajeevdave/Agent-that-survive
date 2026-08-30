"""Conversation memory and session store module."""
from typing import Any, Optional
from agentic_patterns.llm.providers.base import Message


class ConversationMemory:
    def __init__(self, session_id: str = "default", metadata: Optional[dict[str, Any]] = None):
        self.session_id = session_id
        self.metadata = metadata or {}
        self.messages: list[Message] = []
        self.memory_store: dict[str, Any] = {}

    def add_message(self, role: str, content: str) -> None:
        self.messages.append(Message(role=role, content=content))

    def add_user_message(self, content: str) -> None:
        self.add_message("user", content)

    def add_assistant_message(self, content: str) -> None:
        self.add_message("assistant", content)

    def get_messages(self) -> list[Message]:
        return self.messages

    def get_messages_for_model(self, system_prompt: str = "") -> list[Message]:
        res = []
        if system_prompt:
            res.append(Message(role="system", content=system_prompt))
        res.extend(self.messages)
        return res

    def remember(self, key: str, value: Any) -> None:
        self.memory_store[key] = value

    def recall(self, key: str, default: Any = None) -> Any:
        return self.memory_store.get(key, default)

    def clear(self) -> None:
        self.messages.clear()
        self.memory_store.clear()


class InMemorySessionStore:
    def __init__(self) -> None:
        self._store: dict[str, ConversationMemory] = {}

    def get_or_create(self, session_id: str, metadata: Optional[dict[str, Any]] = None) -> ConversationMemory:
        if session_id not in self._store:
            self._store[session_id] = ConversationMemory(session_id=session_id, metadata=metadata)
        return self._store[session_id]

    def save(self, memory: ConversationMemory) -> None:
        self._store[memory.session_id] = memory
