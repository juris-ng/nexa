# NEXA Simulation Test Script
# Run this to test 24 simulated hours

Set-Location "NEXA\simulation\engines"

python -c "from world_clock import WorldClock; clock = WorldClock(seconds_per_minute=1); print('Starting simulation...'); print(f'Day {clock.get_day()}, Time: {clock.get_time_str()}'); clock.run(duration_seconds=30); print(f'After 30 seconds: Day {clock.get_day()}, Time: {clock.get_time_str()}'); print('Simulation test complete!')"
