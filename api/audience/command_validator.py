from typing import Any, Dict, Tuple

from command_models import (
    AudienceCommand,
    CommandIntent,
    CommandStatus,
)
from player_models import PlayerProfile


class CommandValidator:
    """
    Validates audience commands before any execution.

    No command is allowed to run arbitrary code, execute SQL,
    access the server shell, or directly modify world state.
    """

    def validate(
        self,
        command: AudienceCommand,
        player: PlayerProfile,
        world_state: Dict[str, Any],
    ) -> Tuple[bool, str]:
        if command.intent == CommandIntent.UNKNOWN:
            command.status = CommandStatus.REJECTED
            command.validation_reason = (
                "The command intent could not be recognised."
            )
            return False, command.validation_reason

        if command.target_id is None:
            command.status = CommandStatus.REJECTED
            command.validation_reason = (
                "The command target could not be resolved."
            )
            return False, command.validation_reason

        if player.reputation < 5.0:
            command.status = CommandStatus.REJECTED
            command.validation_reason = (
                "Player reputation is too low to perform this action."
            )
            return False, command.validation_reason

        if command.intent == CommandIntent.INVESTIGATE:
            if command.target_id != "eastern_warehouse":
                command.status = CommandStatus.REJECTED
                command.validation_reason = (
                    "That location is not currently available for investigation."
                )
                return False, command.validation_reason

        if command.intent == CommandIntent.TALK:
            if command.target_id != "mayor_elena":
                command.status = CommandStatus.REJECTED
                command.validation_reason = (
                    "That character is not available for a conversation."
                )
                return False, command.validation_reason

        if command.intent == CommandIntent.FOLLOW:
            if command.target_id != "journalist_malik":
                command.status = CommandStatus.REJECTED
                command.validation_reason = (
                    "That character cannot currently be followed."
                )
                return False, command.validation_reason

        if command.intent == CommandIntent.EXPOSE:
            if command.target_id != "nexa_corporation":
                command.status = CommandStatus.REJECTED
                command.validation_reason = (
                    "There is no valid public exposure action for this target."
                )
                return False, command.validation_reason

            if player.influence < 10.0:
                command.status = CommandStatus.REJECTED
                command.validation_reason = (
                    "More influence or evidence is required before a public exposure."
                )
                return False, command.validation_reason

        if command.intent == CommandIntent.ASK_NIA:
            command.status = CommandStatus.VALIDATED
            command.validation_reason = "NIA question authorised."
            return True, command.validation_reason

        if world_state.get("simulation_day", 0) < 1:
            command.status = CommandStatus.REJECTED
            command.validation_reason = "The NEXA world is not active."
            return False, command.validation_reason

        command.status = CommandStatus.VALIDATED
        command.validation_reason = "Command passed permissions and world rules."
        return True, command.validation_reason
