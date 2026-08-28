from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid


class MemoryType(str, Enum):
    SHORT_TERM = "short_term"
    EPISODIC = "episodic"
    SEMANTIC = "semantic"
    RELATIONSHIP = "relationship"
    SECRET = "secret"


@dataclass
class Memory:
    """
    A compact persistent NIA memory record.

    Score ranges:
    - importance: 0 to 100
    - emotional_weight: 0 to 100
    - recency: calculated dynamically at retrieval time
    - relationship: 0 to 100
    - secrecy: 0 to 100
    """

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    memory_type: MemoryType = MemoryType.EPISODIC
    content: str = ""
    subject_ids: List[str] = field(default_factory=list)
    event_id: Optional[str] = None
    importance: float = 50.0
    emotional_weight: float = 50.0
    relationship: float = 50.0
    secrecy: float = 0.0
    allowed_audience: List[str] = field(
        default_factory=lambda: ["NIA"]
    )
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    @staticmethod
    def clamp(value: float) -> float:
        return max(0.0, min(100.0, round(float(value), 2)))

    def calculate_recency(
        self,
        current_time: Optional[datetime] = None,
    ) -> float:
        if current_time is None:
            current_time = datetime.now(timezone.utc)

        created_at = self.created_at

        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=timezone.utc)

        hours_old = max(
            0.0,
            (current_time - created_at).total_seconds() / 3600,
        )

        return self.clamp(100.0 / (1.0 + hours_old / 24.0))

    def is_authorised_for(
        self,
        requester: str,
        clearance: float = 0.0,
    ) -> bool:
        if requester == "NIA":
            return True

        if requester in self.allowed_audience:
            return clearance >= self.secrecy

        return self.secrecy == 0.0

    def to_dict(
        self,
        include_content: bool = True,
    ) -> Dict[str, Any]:
        data = {
            "id": self.id,
            "memory_type": self.memory_type.value,
            "subject_ids": self.subject_ids,
            "event_id": self.event_id,
            "importance": self.importance,
            "emotional_weight": self.emotional_weight,
            "recency": self.calculate_recency(),
            "relationship": self.relationship,
            "secrecy": self.secrecy,
            "allowed_audience": self.allowed_audience,
            "tags": self.tags,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

        if include_content:
            data["content"] = self.content

        return data
