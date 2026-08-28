from typing import Dict, Any
from datetime import datetime

class PublicOpinionSystem:
    """
    NEXA Public Opinion Simulation
    Handles government, corporations, factions, NIA, player, major events.
    """
    
    def __init__(self, db_connection):
        self.db = db_connection
        self.state = {
            "government": 50.0,
            "corporations": 50.0,
            "factions": 50.0,
            "nia": 50.0,
            "player": 50.0,
            "major_events": []
        }
    
    def tick(self, day: int, sim_time: datetime):
        """Update public opinion state."""
        self._update_opinions()
    
    def _update_opinions(self):
        """Adjust opinion scores."""
        import random
        for key in ["government", "corporations", "factions", "nia", "player"]:
            self.state[key] += random.uniform(-1, 1)
            self.state[key] = max(0, min(100, self.state[key]))
    
    def get_state(self) -> Dict[str, Any]:
        return self.state.copy()