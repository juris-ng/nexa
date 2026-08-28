from typing import Dict, Any
from datetime import datetime

class EconomySystem:
    """
    NEXA Economy Simulation
    Handles prices, supply, demand, employment, income, businesses, taxes, wealth.
    """
    
    def __init__(self, db_connection):
        self.db = db_connection
        self.state = {
            "prices": 100.0,
            "supply": 100.0,
            "demand": 100.0,
            "employment": 90.0,
            "income": 50000.0,
            "businesses": 100,
            "taxes": 20.0,
            "wealth": 1000000.0
        }
    
    def tick(self, day: int, sim_time: datetime):
        """Update economy state."""
        self._update_supply_demand()
        self._update_prices()
        self._update_employment()
        self._update_income()
        self._update_wealth()
    
    def _update_supply_demand(self):
        """Adjust supply and demand based on simulation factors."""
        import random
        self.state["supply"] += random.uniform(-2, 2)
        self.state["demand"] += random.uniform(-2, 2)
        self.state["supply"] = max(0, min(200, self.state["supply"]))
        self.state["demand"] = max(0, min(200, self.state["demand"]))
    
    def _update_prices(self):
        """Adjust prices based on supply/demand ratio."""
        ratio = self.state["demand"] / max(1, self.state["supply"])
        self.state["prices"] *= (0.99 + (ratio - 1) * 0.01)
        self.state["prices"] = max(10, min(500, self.state["prices"]))
    
    def _update_employment(self):
        """Adjust employment based on economic activity."""
        import random
        self.state["employment"] += random.uniform(-0.5, 0.5)
        self.state["employment"] = max(0, min(100, self.state["employment"]))
    
    def _update_income(self):
        """Adjust income based on employment and prices."""
        employment_factor = self.state["employment"] / 100
        price_factor = 100 / max(1, self.state["prices"])
        self.state["income"] = 50000 * employment_factor * price_factor
    
    def _update_wealth(self):
        """Adjust total wealth."""
        self.state["wealth"] += self.state["income"] * 0.01
    
    def get_state(self) -> Dict[str, Any]:
        return self.state.copy()