from typing import Any, Dict, List

from world_tools import WorldTools


class ContextManager:
    """
    Builds a minimal, relevant and authorised context package for NIA.
    """

    def __init__(self, world_tools: WorldTools) -> None:
        self.world_tools = world_tools

    def build_context(
        self,
        user_message: str,
        player_id: str | None = None,
    ) -> Dict[str, Any]:
        message = user_message.lower()

        context: Dict[str, Any] = {
            "world_state": self.world_tools.get_world_state(),
            "recent_events": self.world_tools.get_recent_events(limit=5),
            "relevant_locations": [],
            "relevant_characters": [],
            "relevant_factions": [],
            "memories": self.world_tools.search_memory(user_message),
            "player_profile": None,
        }

        if player_id:
            context["player_profile"] = (
                self.world_tools.get_player_profile(player_id)
            )

        location_keywords = {
            "warehouse": "eastern_warehouse",
            "square": "city_square",
            "city square": "city_square",
        }

        character_keywords = {
            "mayor": "mayor_elena",
            "elena": "mayor_elena",
            "malik": "journalist_malik",
            "journalist": "journalist_malik",
        }

        faction_keywords = {
            "government": "government",
            "union": "union",
            "workers": "union",
        }

        for keyword, location_id in location_keywords.items():
            if keyword in message:
                location = self.world_tools.get_location(location_id)
                if location:
                    context["relevant_locations"].append(location)

        for keyword, character_id in character_keywords.items():
            if keyword in message:
                character = self.world_tools.get_character(character_id)
                if character:
                    context["relevant_characters"].append(character)

        for keyword, faction_id in faction_keywords.items():
            if keyword in message:
                faction = self.world_tools.get_faction(faction_id)
                if faction:
                    context["relevant_factions"].append(faction)

        return context

    @staticmethod
    def summarise_context(context: Dict[str, Any]) -> str:
        world_state = context["world_state"]
        events: List[Dict[str, Any]] = context["recent_events"]

        event_summary = "No public events are currently recorded."
        if events:
            latest_event = events[-1]
            event_summary = (
                f"Latest public event: {latest_event['type']} — "
                f"{latest_event['cause']}"
            )

        return (
            f"Day {world_state['simulation_day']}, "
            f"{world_state['simulation_time']}. "
            f"Weather: {world_state['weather']}. "
            f"Mayor approval: {world_state['mayor_approval']}. "
            f"Unemployment: {world_state['unemployment_rate']}%. "
            f"{event_summary}"
        )
