from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List


@dataclass
class ConversationMessage:
    speaker: str
    content: str
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def to_dict(self) -> Dict[str, str]:
        return {
            "speaker": self.speaker,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
        }


class ConversationMemory:
    """
    Short-term memory for the active conversation only.
    """

    def __init__(self, maximum_messages: int = 12) -> None:
        self.maximum_messages = maximum_messages
        self.messages: List[ConversationMessage] = []

    def add_message(
        self,
        speaker: str,
        content: str,
    ) -> ConversationMessage:
        message = ConversationMessage(
            speaker=speaker,
            content=content,
        )

        self.messages.append(message)

        if len(self.messages) > self.maximum_messages:
            self.messages = self.messages[-self.maximum_messages:]

        return message

    def get_recent_messages(
        self,
        limit: int = 8,
    ) -> List[Dict[str, str]]:
        return [
            message.to_dict()
            for message in self.messages[-limit:]
        ]

    def clear(self) -> None:
        self.messages = []
