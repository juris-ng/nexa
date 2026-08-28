from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid


class PollStatus(str, Enum):
    OPEN = "open"
    CLOSED = "closed"
    EXECUTED = "executed"


@dataclass
class PollOption:
    id: str
    label: str
    votes: int = 0
    consequence: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "label": self.label,
            "votes": self.votes,
            "consequence": self.consequence,
        }


@dataclass
class AudiencePoll:
    """
    A collective NEXA audience decision.
    """

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    question: str = ""
    options: List[PollOption] = field(default_factory=list)
    deadline: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
        + timedelta(minutes=10)
    )
    status: PollStatus = PollStatus.OPEN
    votes_by_player: Dict[str, str] = field(default_factory=dict)
    result_option_id: Optional[str] = None
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def is_open(self) -> bool:
        return (
            self.status == PollStatus.OPEN
            and datetime.now(timezone.utc) < self.deadline
        )

    def get_option(self, option_id: str) -> Optional[PollOption]:
        for option in self.options:
            if option.id == option_id:
                return option

        return None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "question": self.question,
            "options": [
                option.to_dict()
                for option in self.options
            ],
            "deadline": self.deadline.isoformat(),
            "status": self.status.value,
            "votes_by_player": self.votes_by_player,
            "result_option_id": self.result_option_id,
            "created_at": self.created_at.isoformat(),
        }
