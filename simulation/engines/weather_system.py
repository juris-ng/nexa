from typing import Dict, Any
from datetime import datetime
import random

class WeatherSystem:
    """
    NEXA Weather Simulation
    Handles sunny, cloudy, rain, storm.
    """
    
    def __init__(self, db_connection):
        self.db = db_connection
        self.state = {
            "condition": "sunny",
            "temperature": 22.0,
            "humidity": 50.0,
            "wind_speed": 10.0
        }
        self.conditions = ["sunny", "cloudy", "rain", "storm"]
    
    def tick(self, day: int, sim_time: datetime):
        """Update weather state."""
        self._update_weather()
    
    def _update_weather(self):
        """Change weather conditions."""
        if random.random() < 0.05:
            self.state["condition"] = random.choice(self.conditions)
        
        self.state["temperature"] += random.uniform(-1, 1)
        self.state["temperature"] = max(-10, min(40, self.state["temperature"]))
        
        self.state["humidity"] += random.uniform(-2, 2)
        self.state["humidity"] = max(0, min(100, self.state["humidity"]))
        
        self.state["wind_speed"] += random.uniform(-1, 1)
        self.state["wind_speed"] = max(0, min(50, self.state["wind_speed"]))
    
    def get_state(self) -> Dict[str, Any]:
        return self.state.copy()