from typing import Dict, Any
from datetime import datetime

class TrafficSystem:
    """
    NEXA Traffic Simulation
    Handles traffic_volume, road_capacity, congestion.
    """
    
    def __init__(self, db_connection):
        self.db = db_connection
        self.state = {
            "traffic_volume": 50.0,
            "road_capacity": 100.0,
            "congestion": 30.0
        }
    
    def tick(self, day: int, sim_time: datetime):
        """Update traffic state."""
        hour = sim_time.hour
        self._update_traffic_volume(hour)
        self._update_congestion()
    
    def _update_traffic_volume(self, hour: int):
        """Adjust traffic based on time of day."""
        import random
        if 7 <= hour <= 9 or 17 <= hour <= 19:
            self.state["traffic_volume"] = 80 + random.uniform(-10, 10)
        else:
            self.state["traffic_volume"] = 40 + random.uniform(-10, 10)
    
    def _update_congestion(self):
        """Calculate congestion based on volume and capacity."""
        ratio = self.state["traffic_volume"] / max(1, self.state["road_capacity"])
        self.state["congestion"] = min(100, ratio * 100)
    
    def get_state(self) -> Dict[str, Any]:
        return self.state.copy()