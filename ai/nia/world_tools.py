from typing import Any, Dict, List, Optional

from permissions import PermissionLevel, PermissionManager
from request_queue import RequestQueue


class WorldTools:
    """
    Controlled NIA access to NEXA world information.

    This Phase 7 implementation is intentionally read-only,
    except for creating a pending request.
    """

    def __init__(self, request_queue: RequestQueue) -> None:
        self.permissions = PermissionManager()
        self.request_queue = request_queue

        self.world_state = {
            "simulation_day": 1,
            "simulation_time": "08:00",
            "mayor_approval": 50.0,
            "food_prices_change": 0.0,
            "unemployment_rate": 10.0,
            "union_anger": 50.0,
            "crime_rate": 20.0,
            "weather": "sunny",
        }

        self.locations = {
            "city_square": {
                "id": "city_square",
                "name": "City Square",
                "district": "Central District",
                "type": "public_square",
                "access_level": "public",
                "importance": 85.0,
            },
            "eastern_warehouse": {
                "id": "eastern_warehouse",
                "name": "Eastern Warehouse",
                "district": "Industrial District",
                "type": "warehouse",
                "access_level": "restricted",
                "importance": 78.0,
            },
        }

        self.characters = {
            "mayor_elena": {
                "id": "mayor_elena",
                "name": "Mayor Elena Voss",
                "occupation": "Mayor",
                "location": "city_square",
                "faction": "government",
                "reputation": 50.0,
                "current_activity": "public briefing",
            },
            "journalist_malik": {
                "id": "journalist_malik",
                "name": "Malik Okoro",
                "occupation": "Journalist",
                "location": "city_square",
                "faction": "independent_media",
                "reputation": 62.0,
                "current_activity": "investigating a labour dispute",
            },
        }

        self.factions = {
            "government": {
                "id": "government",
                "name": "City Government",
                "ideology": "Civic stability and public order",
                "public_support": 50.0,
                "political_power": 72.0,
            },
            "union": {
                "id": "union",
                "name": "Workers Union",
                "ideology": "Worker rights and economic justice",
                "public_support": 54.0,
                "political_power": 48.0,
            },
        }

        self.events = [
            {
                "id": "event_001",
                "type": "labour_dispute",
                "cause": "A corporation announced workforce reductions.",
                "location": "eastern_warehouse",
                "importance": 5,
                "visibility": "public",
                "simulation_time": "Day 1, 07:30",
            }
        ]

        self.players = {}
        self.memories = []
        self.evidence = {}

    def get_world_state(self) -> Dict[str, Any]:
        self.permissions.require("get_world_state", PermissionLevel.READ)
        return self.world_state.copy()

    def get_location(self, location_id: str) -> Optional[Dict[str, Any]]:
        self.permissions.require("get_location", PermissionLevel.READ)
        return self.locations.get(location_id)

    def get_character(self, character_id: str) -> Optional[Dict[str, Any]]:
        self.permissions.require("get_character", PermissionLevel.READ)
        return self.characters.get(character_id)

    def get_faction(self, faction_id: str) -> Optional[Dict[str, Any]]:
        self.permissions.require("get_faction", PermissionLevel.READ)
        return self.factions.get(faction_id)

    def get_recent_events(self, limit: int = 10) -> List[Dict[str, Any]]:
        self.permissions.require("get_recent_events", PermissionLevel.READ)
        return self.events[-limit:]

    def get_player_profile(
        self,
        player_id: str,
    ) -> Optional[Dict[str, Any]]:
        self.permissions.require("get_player_profile", PermissionLevel.READ)
        return self.players.get(player_id)

    def search_memory(self, query: str) -> List[Dict[str, Any]]:
        self.permissions.require("search_memory", PermissionLevel.READ)
        query_lower = query.lower()

        return [
            memory
            for memory in self.memories
            if query_lower in str(memory).lower()
        ]

    def inspect_evidence(
        self,
        evidence_id: str,
    ) -> Optional[Dict[str, Any]]:
        self.permissions.require("inspect_evidence", PermissionLevel.READ)
        return self.evidence.get(evidence_id)

    def create_request(
        self,
        request_type: str,
        payload: Dict[str, Any],
        reason: str,
    ) -> Dict[str, Any]:
        self.permissions.require("create_request", PermissionLevel.REQUEST)

        request = self.request_queue.create_request(
            request_type=request_type,
            payload=payload,
            reason=reason,
        )
        return request.to_dict()

    def trigger_event(self, *args: Any, **kwargs: Any) -> None:
        self.permissions.require(
            "trigger_event",
            PermissionLevel.APPROVED_ACTION,
        )

    def send_message(self, *args: Any, **kwargs: Any) -> None:
        self.permissions.require(
            "send_message",
            PermissionLevel.APPROVED_ACTION,
        )

    def change_relationship(self, *args: Any, **kwargs: Any) -> None:
        self.permissions.require(
            "change_relationship",
            PermissionLevel.APPROVED_ACTION,
        )

    def request_camera_focus(self, *args: Any, **kwargs: Any) -> None:
        self.permissions.require(
            "request_camera_focus",
            PermissionLevel.APPROVED_ACTION,
        )
