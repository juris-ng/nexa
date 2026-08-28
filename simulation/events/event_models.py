from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional
from enum import Enum
import uuid

class EventSeverity(Enum):
    TRIVIAL = 1
    MINOR = 2
    LOCAL = 3
    SIGNIFICANT = 4
    MAJOR = 5
    CITY_WIDE = 6
    CRISIS = 7
    HISTORIC = 8

class EventVisibility(Enum):
    PUBLIC = "public"
    RESTRICTED = "restricted"
    SECRET = "secret"

class ConsequenceDelay(Enum):
    IMMEDIATE = "immediate"
    HOURS_LATER = "hours_later"
    DAYS_LATER = "days_later"
    WEEKS_LATER = "weeks_later"

@dataclass
class Event:
    """NEXA Event Object"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str = "generic"
    cause: str = ""
    actors: List[str] = field(default_factory=list)
    location_id: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    visibility: EventVisibility = EventVisibility.PUBLIC
    importance: int = 1
    evidence: Dict[str, Any] = field(default_factory=dict)
    consequences: List[Dict[str, Any]] = field(default_factory=list)
    related_factions: List[str] = field(default_factory=list)
    related_mysteries: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    simulation_time: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "event_type": self.event_type,
            "cause": self.cause,
            "actors": self.actors,
            "location_id": self.location_id,
            "timestamp": self.timestamp.isoformat(),
            "visibility": self.visibility.value,
            "importance": self.importance,
            "evidence": self.evidence,
            "consequences": self.consequences,
            "related_factions": self.related_factions,
            "related_mysteries": self.related_mysteries,
            "created_at": self.created_at.isoformat(),
            "simulation_time": self.simulation_time.isoformat() if self.simulation_time else None
        }

@dataclass
class Consequence:
    """NEXA Consequence Object"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_id: str = ""
    consequence_type: str = "effect"
    target_type: str = "world"
    target_id: Optional[str] = None
    effect: Dict[str, Any] = field(default_factory=dict)
    delay_type: ConsequenceDelay = ConsequenceDelay.IMMEDIATE
    executed: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    simulation_time: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "event_id": self.event_id,
            "consequence_type": self.consequence_type,
            "target_type": self.target_type,
            "target_id": self.target_id,
            "effect": self.effect,
            "delay_type": self.delay_type.value,
            "executed": self.executed,
            "created_at": self.created_at.isoformat(),
            "simulation_time": self.simulation_time.isoformat() if self.simulation_time else None
        }