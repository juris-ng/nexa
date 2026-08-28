from typing import Dict, Any
from datetime import datetime

class CrimeSystem:
    """
    NEXA Crime Simulation
    Handles crime probability, police presence, criminal organizations, response.
    """
    
    def __init__(self, db_connection):
        self.db = db_connection
        self.state = {
            "crime_probability": 20.0,
            "police_presence": 50.0,
            "criminal_organizations": 3,
            "response_time": 5.0
        }
    
    def tick(self, day: int, sim_time: datetime):
        """Update crime state."""
        self._update_crime_probability()
        self._update_police_presence()
        self._update_response_time()
    
    def _update_crime_probability(self):
        """Adjust crime probability based on social factors."""
        import random
        self.state["crime_probability"] += random.uniform(-1, 1)
        self.state["crime_probability"] = max(0, min(100, self.state["crime_probability"]))
    
    def _update_police_presence(self):
        """Adjust police presence."""
        import random
        self.state["police_presence"] += random.uniform(-0.5, 0.5)
        self.state["police_presence"] = max(0, min(100, self.state["police_presence"]))
    
    def _update_response_time(self):
        """Update emergency response time."""
        presence_factor = 100 / max(1, self.state["police_presence"])
        self.state["response_time"] = 3 * presence_factor
    
    def get_state(self) -> Dict[str, Any]:
        return self.state.copy()