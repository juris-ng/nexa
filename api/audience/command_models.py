from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional
import uuid


class CommandIntent(str, Enum):
    INVESTIGATE = "INVESTIGATE"
    TALK = "TALK"
    FOLLOW = "FOLLOW"
    EXPOSE = "EXPOSE"
    ASK_NIA = "ASK_NIA"
    VOTE = "VOTE"
    UNKNOWN = "UNKNOWN"


class CommandStatus(str, Enum):
    PARSED = "parsed"
    VALIDATED = "validated"
    REJECTED = "rejected"
    EXECUTED = "executed"


@dataclass
class AudienceCommand:
    """
    Structured representation of an audience natural-language command.
    """

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    player_id: str = ""
    raw_text: str = ""
    intent: CommandIntent = CommandIntent.UNKNOWN
    target_type: Optional[str] = None
    target_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    status: CommandStatus = CommandStatus.PARSED
    validation_reason: str = ""
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "player_id": self.player_id,
            "raw_text": self.raw_text,
            "intent": self.intent.value,
            "target_type": self.target_type,
            "target_id": self.target_id,
            "metadata": self.metadata,
            "status": self.status.value,
            "validation_reason": self.validation_reason,
            "created_at": self.created_at.isoformat(),
        }
