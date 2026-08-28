# NEXA Event Engine Test Script

Set-Location "$PSScriptRoot"

python -c "from event_engine import EventEngine; engine = EventEngine(None); print('Creating example event...'); event = engine.trigger_example_event(); print(f'Event created: {event.event_type}'); print(f'Cause: {event.cause}'); print(f'Importance: {event.importance}'); print(f'Consequences: {len(event.consequences)}'); print('Event engine test complete!')"
