from typing import Any, Dict, List

from director_models import WorldObservation


class WorldObserver:
    """
    Collects the authorised world inputs required by the AI Director.
    """

    def observe(
        self,
        world_state: Dict[str, Any],
        player_activity: Dict[str, Any] | None = None,
        audience_activity: Dict[str, Any] | None = None,
        active_mysteries: List[Dict[str, Any]] | None = None,
        recent_events: List[Dict[str, Any]] | None = None,
        nia_activity: Dict[str, Any] | None = None,
    ) -> WorldObservation:
        return WorldObservation(
            world_state=world_state,
            player_activity=player_activity or {},
            audience_activity=audience_activity or {},
            active_mysteries=active_mysteries or [],
            recent_events=recent_events or [],
            nia_activity=nia_activity or {},
        )
