from typing import Dict, Any
from datetime import datetime

class PoliticsSystem:
    """
    NEXA Politics Simulation
    Handles approval, elections, factions, policy, corruption, protests.
    """
    
    def __init__(self, db_connection):
        self.db = db_connection
        self.state = {
            "approval": 50.0,
            "elections": None,
            "factions": 5,
            "policy": 50.0,
            "corruption": 30.0,
            "protests": 0
        }
    
    def tick(self, day: int, sim_time: datetime):
        """Update politics state."""
        self._update_approval()
        self._update_corruption()
        self._update_protests()
    
    def _update_approval(self):
        """Adjust government approval."""
        import random
        self.state["approval"] += random.uniform(-1, 1)
        self.state["approval"] = max(0, min(100, self.state["approval"]))
    
    def _update_corruption(self):
        """Adjust corruption level."""
        import random
        self.state["corruption"] += random.uniform(-0.5, 0.5)
        self.state["corruption"] = max(0, min(100, self.state["corruption"]))
    
    def _update_protests(self):
        """Calculate protest activity."""
        import random
        if self.state["approval"] < 30:
            self.state["protests"] = random.randint(1, 5)
        else:
            self.state["protests"] = 0
    
    def get_state(self) -> Dict[str, Any]:
        return self.state.copy()