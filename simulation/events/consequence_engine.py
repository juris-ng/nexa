from event_models import Consequence, ConsequenceDelay
from datetime import datetime, timedelta
from typing import List, Dict, Any

class ConsequenceEngine:
    """
    NEXA Consequence Engine
    Executes consequences with appropriate delays.
    """
    
    def __init__(self, db_connection):
        self.db = db_connection
        self.pending_consequences: List[Consequence] = []
    
    def add_consequence(self, consequence: Consequence):
        """Add a consequence to be executed."""
        if consequence.delay_type == ConsequenceDelay.IMMEDIATE:
            self.execute_consequence(consequence)
        else:
            self.pending_consequences.append(consequence)
    
    def execute_consequence(self, consequence: Consequence):
        """Execute a single consequence."""
        effect = consequence.effect
        target_type = consequence.target_type
        target_id = consequence.target_id
        
        if target_type == "world_state":
            self._apply_world_effect(effect)
        elif target_type == "faction":
            self._apply_faction_effect(target_id, effect)
        elif target_type == "character":
            self._apply_character_effect(target_id, effect)
        elif target_type == "economy":
            self._apply_economy_effect(effect)
        elif target_type == "politics":
            self._apply_politics_effect(effect)
        
        consequence.executed = True
    
    def _apply_world_effect(self, effect: Dict[str, Any]):
        """Apply effect to world state."""
        if "unemployment_rate" in effect:
            pass
        if "crime_rate" in effect:
            pass
        if "approval" in effect:
            pass
    
    def _apply_faction_effect(self, faction_id: str, effect: Dict[str, Any]):
        """Apply effect to a faction."""
        pass
    
    def _apply_character_effect(self, character_id: str, effect: Dict[str, Any]):
        """Apply effect to a character."""
        pass
    
    def _apply_economy_effect(self, effect: Dict[str, Any]):
        """Apply effect to economy."""
        pass
    
    def _apply_politics_effect(self, effect: Dict[str, Any]):
        """Apply effect to politics."""
        pass
    
    def process_pending(self, current_time: datetime):
        """Process pending consequences based on their delay."""
        executed = []
        for consequence in self.pending_consequences:
            if self._should_execute(consequence, current_time):
                self.execute_consequence(consequence)
                executed.append(consequence)
        
        for c in executed:
            self.pending_consequences.remove(c)
    
    def _should_execute(self, consequence: Consequence, current_time: datetime) -> bool:
        """Determine if a consequence should be executed now."""
        delay = consequence.delay_type
        created = consequence.created_at
        
        if delay == ConsequenceDelay.HOURS_LATER:
            return current_time >= created + timedelta(hours=1)
        elif delay == ConsequenceDelay.DAYS_LATER:
            return current_time >= created + timedelta(days=1)
        elif delay == ConsequenceDelay.WEEKS_LATER:
            return current_time >= created + timedelta(weeks=1)
        
        return False