from typing import Dict, Any
from datetime import datetime

class PopulationSystem:
    """
    NEXA Population Simulation
    Handles birth, death, migration, employment, housing, consumption.
    """
    
    def __init__(self, db_connection):
        self.db = db_connection
        self.state = {
            "population": 500,
            "birth_rate": 1.2,
            "death_rate": 0.8,
            "migration": 0,
            "employment": 90.0,
            "housing": 95.0,
            "consumption": 100.0
        }
    
    def tick(self, day: int, sim_time: datetime):
        """Update population state."""
        self._update_birth_death()
        self._update_migration()
        self._update_housing()
        self._update_consumption()
    
    def _update_birth_death(self):
        """Calculate population changes."""
        import random
        births = (self.state["birth_rate"] / 100) * self.state["population"] * 0.01
        deaths = (self.state["death_rate"] / 100) * self.state["population"] * 0.01
        self.state["population"] += births - deaths + random.uniform(-1, 1)
        self.state["population"] = max(100, min(10000, self.state["population"]))
    
    def _update_migration(self):
        """Calculate net migration."""
        import random
        self.state["migration"] = random.uniform(-5, 5)
    
    def _update_housing(self):
        """Update housing availability."""
        import random
        self.state["housing"] += random.uniform(-0.5, 0.5)
        self.state["housing"] = max(0, min(100, self.state["housing"]))
    
    def _update_consumption(self):
        """Update consumption based on population and employment."""
        employment_factor = self.state["employment"] / 100
        self.state["consumption"] = 100 * employment_factor * (self.state["population"] / 500)
    
    def get_state(self) -> Dict[str, Any]:
        return self.state.copy()