from datetime import datetime, timedelta
from typing import Callable, List
import time

class WorldClock:
    """
    NEXA World Clock
    Controls simulation time progression.
    
    Default: 1 real second = 1 simulated minute
    Adjust acceleration as needed.
    """
    
    def __init__(self, seconds_per_minute: int = 1):
        self.simulation_day: int = 1
        self.simulation_time: datetime = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        self.seconds_per_minute: int = seconds_per_minute
        self.last_tick: float = time.time()
        self.callbacks: List[Callable] = []
        self.running: bool = False
    
    def tick(self):
        """Advance simulation by one minute."""
        self.simulation_time += timedelta(minutes=1)
        
        if self.simulation_time.hour == 0 and self.simulation_time.minute == 0:
            self.simulation_day += 1
        
        self.last_tick = time.time()
        
        for callback in self.callbacks:
            callback(self.simulation_day, self.simulation_time)
    
    def get_time(self) -> datetime:
        return self.simulation_time
    
    def get_day(self) -> int:
        return self.simulation_day
    
    def get_time_str(self) -> str:
        return self.simulation_time.strftime("%H:%M:%S")
    
    def register_callback(self, callback: Callable):
        """Register a function to call on each tick."""
        self.callbacks.append(callback)
    
    def start(self):
        """Start the simulation clock."""
        self.running = True
    
    def stop(self):
        """Stop the simulation clock."""
        self.running = False
    
    def run(self, duration_seconds: int = None):
        """Run the clock for a specified duration or indefinitely."""
        self.running = True
        start_time = time.time()
        
        try:
            while self.running:
                current_time = time.time()
                if current_time - self.last_tick >= self.seconds_per_minute:
                    self.tick()
                
                if duration_seconds and (current_time - start_time) >= duration_seconds:
                    break
                
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.stop()