from event_models import Event, Consequence, EventSeverity, EventVisibility, ConsequenceDelay
from event_types import EventType
from consequence_engine import ConsequenceEngine
from datetime import datetime
from typing import List, Dict, Any, Optional

class EventEngine:
    """
    NEXA Event Engine
    Creates events and propagates consequences through the world.
    
    Architecture:
    CAUSE → EVENT → CONSEQUENCES → WORLD STATE → SECONDARY EVENTS
    """
    
    def __init__(self, db_connection):
        self.db = db_connection
        self.consequence_engine = ConsequenceEngine(db_connection)
        self.events: List[Event] = []
    
    def create_event(
        self,
        event_type: str,
        cause: str,
        actors: List[str] = None,
        location_id: Optional[str] = None,
        importance: int = 3,
        visibility: EventVisibility = EventVisibility.PUBLIC,
        evidence: Dict[str, Any] = None,
        related_factions: List[str] = None,
        related_mysteries: List[str] = None
    ) -> Event:
        """Create a new event."""
        event = Event(
            event_type=event_type,
            cause=cause,
            actors=actors or [],
            location_id=location_id,
            importance=importance,
            visibility=visibility,
            evidence=evidence or {},
            related_factions=related_factions or [],
            related_mysteries=related_mysteries or []
        )
        
        self.events.append(event)
        return event
    
    def add_consequence(
        self,
        event: Event,
        consequence_type: str,
        target_type: str,
        target_id: Optional[str],
        effect: Dict[str, Any],
        delay_type: ConsequenceDelay = ConsequenceDelay.IMMEDIATE
    ):
        """Add a consequence to an event."""
        consequence = Consequence(
            event_id=event.id,
            consequence_type=consequence_type,
            target_type=target_type,
            target_id=target_id,
            effect=effect,
            delay_type=delay_type
        )
        
        event.consequences.append(consequence.to_dict())
        self.consequence_engine.add_consequence(consequence)
    
    def trigger_example_event(self):
        """
        Example: Corporation fires 300 workers
        Demonstrates consequence propagation.
        """
        event = self.create_event(
            event_type="economic",
            cause="Corporation fires 300 workers",
            importance=5,
            visibility=EventVisibility.PUBLIC
        )
        
        self.add_consequence(
            event=event,
            consequence_type="unemployment_increase",
            target_type="world_state",
            target_id=None,
            effect={"unemployment_rate": 5.0},
            delay_type=ConsequenceDelay.IMMEDIATE
        )
        
        self.add_consequence(
            event=event,
            consequence_type="union_anger_increase",
            target_type="faction",
            target_id="union_faction_id",
            effect={"anger": 25.0},
            delay_type=ConsequenceDelay.HOURS_LATER
        )
        
        self.add_consequence(
            event=event,
            consequence_type="protest_probability_increase",
            target_type="world_state",
            target_id=None,
            effect={"protest_probability": 40.0},
            delay_type=ConsequenceDelay.DAYS_LATER
        )
        
        return event
    
    def get_events(self) -> List[Event]:
        return self.events
    
    def get_event_by_id(self, event_id: str) -> Optional[Event]:
        for event in self.events:
            if event.id == event_id:
                return event
        return None