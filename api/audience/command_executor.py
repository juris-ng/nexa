from datetime import datetime, timezone
from typing import Any, Dict

from command_models import (
    AudienceCommand,
    CommandIntent,
    CommandStatus,
)
from player_models import PlayerProfile


class CommandExecutor:
    """
    Executes only already validated and explicitly supported actions.
    """

    @staticmethod
    def _clamp(value: float) -> float:
        return max(0.0, min(100.0, round(value, 2)))

    def execute(
        self,
        command: AudienceCommand,
        player: PlayerProfile,
        world_state: Dict[str, Any],
    ) -> Dict[str, Any]:
        if command.status != CommandStatus.VALIDATED:
            raise ValueError(
                "A command must be validated before execution."
            )

        result: Dict[str, Any] = {
            "command_id": command.id,
            "intent": command.intent.value,
            "target_id": command.target_id,
            "world_changes": {},
            "player_changes": {},
            "message": "",
            "executed_at": datetime.now(timezone.utc).isoformat(),
        }

        if command.intent == CommandIntent.INVESTIGATE:
            world_state["audience_investigations"] = (
                int(world_state.get("audience_investigations", 0)) + 1
            )
            world_state["mystery_attention"] = self._clamp(
                float(world_state.get("mystery_attention", 0.0)) + 12.0
            )

            player.change_reputation(3.0)
            player.change_influence(2.0)
            player.add_achievement("First Investigation")

            result["world_changes"] = {
                "audience_investigations": (
                    world_state["audience_investigations"]
                ),
                "mystery_attention": world_state["mystery_attention"],
            }
            result["player_changes"] = {
                "reputation_change": 3.0,
                "influence_change": 2.0,
            }
            result["message"] = (
                "Investigation authorised. Audience attention is now focused "
                "on the Eastern Warehouse."
            )

        elif command.intent == CommandIntent.TALK:
            world_state["mayor_contact_requests"] = (
                int(world_state.get("mayor_contact_requests", 0)) + 1
            )
            player.change_reputation(1.0)

            result["world_changes"] = {
                "mayor_contact_requests": (
                    world_state["mayor_contact_requests"]
                ),
            }
            result["player_changes"] = {
                "reputation_change": 1.0,
            }
            result["message"] = (
                "A meeting request has been added to the mayor's schedule."
            )

        elif command.intent == CommandIntent.FOLLOW:
            world_state["journalist_followers"] = (
                int(world_state.get("journalist_followers", 0)) + 1
            )
            world_state["mystery_attention"] = self._clamp(
                float(world_state.get("mystery_attention", 0.0)) + 5.0
            )

            result["world_changes"] = {
                "journalist_followers": world_state["journalist_followers"],
                "mystery_attention": world_state["mystery_attention"],
            }
            result["message"] = (
                "The journalist is now being followed as part of the investigation."
            )

        elif command.intent == CommandIntent.EXPOSE:
            world_state["corporate_scrutiny"] = self._clamp(
                float(world_state.get("corporate_scrutiny", 0.0)) + 15.0
            )
            player.change_reputation(5.0)
            player.change_influence(5.0)
            player.add_achievement("Corporate Watchdog")

            result["world_changes"] = {
                "corporate_scrutiny": world_state["corporate_scrutiny"],
            }
            result["player_changes"] = {
                "reputation_change": 5.0,
                "influence_change": 5.0,
            }
            result["message"] = (
                "The corporation has been placed under increased public scrutiny."
            )

        elif command.intent == CommandIntent.ASK_NIA:
            result["message"] = (
                "The question has been routed to NIA's controlled "
                "context-and-memory system."
            )

        else:
            raise ValueError(
                f"Execution is not implemented for {command.intent.value}."
            )

        player.record_action(
            {
                "command_id": command.id,
                "intent": command.intent.value,
                "target_id": command.target_id,
                "result": result["message"],
            }
        )

        command.status = CommandStatus.EXECUTED
        return result
