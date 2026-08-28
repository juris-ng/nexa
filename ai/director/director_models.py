from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List
import uuid


class ProposalStatus(str, Enum):
    PROPOSED = "proposed"
    SCHEDULED = "scheduled"
    VALIDATED = "validated"
    REJECTED = "rejected"
    EXECUTED = "executed"


@dataclass
class WorldObservation:
    """
    Snapshot of the inputs the AI Director observes.
    """

    world_state: Dict[str, Any]
    player_activity: Dict[str, Any] = field(default_factory=dict)
    audience_activity: Dict[str, Any] = field(default_factory=dict)
    active_mysteries: List[Dict[str, Any]] = field(default_factory=list)
    recent_events: List[Dict[str, Any]] = field(default_factory=list)
    nia_activity: Dict[str, Any] = field(default_factory=dict)
    observed_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


@dataclass
class DirectorMetrics:
    """
    Scores used by the Director to assess entertainment state.
    All scores range from 0 to 100.
    """

    interest: float = 0.0
    tension: float = 0.0
    novelty: float = 0.0
    importance: float = 0.0
    mystery_potential: float = 0.0
    audience_engagement: float = 0.0
    pacing: float = 0.0

    def to_dict(self) -> Dict[str, float]:
        return {
            "interest": self.interest,
            "tension": self.tension,
            "novelty": self.novelty,
            "importance": self.importance,
            "mystery_potential": self.mystery_potential,
            "audience_engagement": self.audience_engagement,
            "pacing": self.pacing,
        }


@dataclass
class EventProposal:
    """
    A Director proposal is not an executed event.
    It must later pass NEXA simulation and event validation.
    """

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str = "general"
    title: str = "Untitled Director Proposal"
    reason: str = ""
    target_location_id: str | None = None
    related_factions: List[str] = field(default_factory=list)
    related_mysteries: List[str] = field(default_factory=list)
    suggested_effects: Dict[str, Any] = field(default_factory=dict)
    priority: float = 0.0
    status: ProposalStatus = ProposalStatus.PROPOSED
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "event_type": self.event_type,
            "title": self.title,
            "reason": self.reason,
            "target_location_id": self.target_location_id,
            "related_factions": self.related_factions,
            "related_mysteries": self.related_mysteries,
            "suggested_effects": self.suggested_effects,
            "priority": round(self.priority, 2),
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
        }
