from world_clock import WorldClock
from economy_system import EconomySystem
from population_system import PopulationSystem
from crime_system import CrimeSystem
from politics_system import PoliticsSystem
from traffic_system import TrafficSystem
from public_opinion_system import PublicOpinionSystem
from weather_system import WeatherSystem
from typing import Dict, Any

class SimulationEngine:
    """
    NEXA Simulation Engine
    Coordinates all simulation systems.
    """
    
    def __init__(self, db_connection):
        self.db = db_connection
        self.clock = WorldClock(seconds_per_minute=1)
        
        self.economy = EconomySystem(db_connection)
        self.population = PopulationSystem(db_connection)
        self.crime = CrimeSystem(db_connection)
        self.politics = PoliticsSystem(db_connection)
        self.traffic = TrafficSystem(db_connection)
        self.opinion = PublicOpinionSystem(db_connection)
        self.weather = WeatherSystem(db_connection)
        
        self.clock.register_callback(self.on_tick)
    
    def on_tick(self, day: int, sim_time):
        """Called on each world tick."""
        self.economy.tick(day, sim_time)
        self.population.tick(day, sim_time)
        self.crime.tick(day, sim_time)
        self.politics.tick(day, sim_time)
        self.traffic.tick(day, sim_time)
        self.opinion.tick(day, sim_time)
        self.weather.tick(day, sim_time)
    
    def get_world_state(self) -> Dict[str, Any]:
        """Return current world state."""
        return {
            "day": self.clock.get_day(),
            "time": self.clock.get_time_str(),
            "economy": self.economy.get_state(),
            "population": self.population.get_state(),
            "crime": self.crime.get_state(),
            "politics": self.politics.get_state(),
            "traffic": self.traffic.get_state(),
            "opinion": self.opinion.get_state(),
            "weather": self.weather.get_state()
        }
    
    def start(self, duration_seconds: int = None):
        """Start the simulation."""
        self.clock.start()
        self.clock.run(duration_seconds)
    
    def stop(self):
        """Stop the simulation."""
        self.clock.stop()