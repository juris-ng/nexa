from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid


class MysteryState(str, Enum):
    HIDDEN = "hidden"
    HINTED = "hinted"
    DISCOVERED = "discovered"
    INVESTIGATED = "investigated"
    PARTIALLY_UNDERSTOOD = "partially_understood"
    NEAR_RESOLUTION = "near_resolution"
    RESOLVED = "resolved"


class EvidenceVisibility(str, Enum):
    HIDDEN = "hidden"
    RESTRICTED = "restricted"
    DISCOVERED = "discovered"
    PUBLIC = "public"


@dataclass
class Evidence:
    """
    A piece of evidence connected to a NEXA mystery.
    """

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = "Untitled Evidence"
    description: str = ""
    source: str = "unknown"
    reliability: float = 50.0
    location_id: Optional[str] = None
    visibility: EvidenceVisibility = EvidenceVisibility.HIDDEN
    linked_character_id: Optional[str] = None
    linked_event_id: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    discovered_at_day: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "source": self.source,
            "reliability": self.reliability,
            "location_id": self.location_id,
            "visibility": self.visibility.value,
            "linked_character_id": self.linked_character_id,
            "linked_event_id": self.linked_event_id,
            "tags": self.tags,
            "created_at": self.created_at.isoformat(),
            "discovered_at_day": self.discovered_at_day,
        }


@dataclass
class StoryBeat:
    """
    A delayed narrative development scheduled for a simulation day.
    """

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    simulation_day: int = 1
    title: str = "Untitled Story Beat"
    description: str = ""
    event_type: str = "narrative"
    target_state: Optional[MysteryState] = None
    reveal_evidence_ids: List[str] = field(default_factory=list)
    related_character_ids: List[str] = field(default_factory=list)
    related_event_ids: List[str] = field(default_factory=list)
    audience_required: bool = False
    nia_discovery: bool = False
    executed: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "simulation_day": self.simulation_day,
            "title": self.title,
            "description": self.description,
            "event_type": self.event_type,
            "target_state": (
                self.target_state.value
                if self.target_state
                else None
            ),
            "reveal_evidence_ids": self.reveal_evidence_ids,
            "related_character_ids": self.related_character_ids,
            "related_event_ids": self.related_event_ids,
            "audience_required": self.audience_required,
            "nia_discovery": self.nia_discovery,
            "executed": self.executed,
        }


@dataclass
class Mystery:
    """
    Persistent long-form NEXA narrative mystery.
    """

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = "Untitled Mystery"
    premise: str = ""
    hidden_truth: str = ""
    suspects: List[str] = field(default_factory=list)
    evidence_ids: List[str] = field(default_factory=list)
    false_leads: List[str] = field(default_factory=list)
    event_ids: List[str] = field(default_factory=list)
    revelations: List[str] = field(default_factory=list)
    resolution: str = ""
    state: MysteryState = MysteryState.HIDDEN
    story_beats: List[StoryBeat] = field(default_factory=list)
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "premise": self.premise,
            "hidden_truth": self.hidden_truth,
            "suspects": self.suspects,
            "evidence_ids": self.evidence_ids,
            "false_leads": self.false_leads,
            "event_ids": self.event_ids,
            "revelations": self.revelations,
            "resolution": self.resolution,
            "state": self.state.value,
            "story_beats": [
                beat.to_dict()
                for beat in self.story_beats
            ],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
