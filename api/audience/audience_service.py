from typing import Any, Dict, List

from command_executor import CommandExecutor
from command_parser import CommandParser
from command_validator import CommandValidator
from player_service import PlayerService
from voting_models import PollOption
from voting_service import VotingService


class AudienceService:
    """
    Main Phase 11 audience participation coordinator.
    """

    def __init__(self, world_state: Dict[str, Any]) -> None:
        self.world_state = world_state
        self.players = PlayerService()
        self.parser = CommandParser()
        self.validator = CommandValidator()
        self.executor = CommandExecutor()
        self.voting = VotingService()

    def create_player(self, name: str) -> Dict[str, Any]:
        return self.players.create_player(name).to_dict()

    def submit_command(
        self,
        player_id: str,
        raw_text: str,
    ) -> Dict[str, Any]:
        player = self.players.get_player(player_id)

        if player is None:
            return {
                "accepted": False,
                "message": "Player profile not found.",
            }

        command = self.parser.parse(player_id, raw_text)

        valid, reason = self.validator.validate(
            command=command,
            player=player,
            world_state=self.world_state,
        )

        if not valid:
            return {
                "accepted": False,
                "command": command.to_dict(),
                "message": reason,
            }

        result = self.executor.execute(
            command=command,
            player=player,
            world_state=self.world_state,
        )

        return {
            "accepted": True,
            "command": command.to_dict(),
            "result": result,
            "player": player.to_dict(),
            "world_state": self.world_state.copy(),
        }

    def create_tax_poll(
        self,
        duration_minutes: int = 10,
    ) -> Dict[str, Any]:
        poll = self.voting.create_poll(
            question="Should NEXA increase taxes?",
            options=[
                PollOption(
                    id="increase_taxes",
                    label="Increase taxes by 2%",
                    consequence={
                        "tax_rate_change": 2.0,
                        "mayor_approval_change": -3.0,
                        "union_anger_change": 2.0,
                        "public_interest_change": 4.0,
                    },
                ),
                PollOption(
                    id="keep_taxes",
                    label="Keep current tax rate",
                    consequence={
                        "public_interest_change": 1.0,
                    },
                ),
            ],
            duration_minutes=duration_minutes,
        )

        return poll.to_dict()

    def cast_vote(
        self,
        poll_id: str,
        player_id: str,
        option_id: str,
    ) -> Dict[str, Any]:
        accepted, message = self.voting.vote(
            poll_id=poll_id,
            player_id=player_id,
            option_id=option_id,
        )

        return {
            "accepted": accepted,
            "message": message,
        }

    def close_and_apply_poll(
        self,
        poll_id: str,
    ) -> Dict[str, Any]:
        winner = self.voting.close_poll(poll_id)

        if winner is None:
            return {
                "accepted": False,
                "message": "Poll could not be closed.",
            }

        result = self.voting.execute_result(
            poll_id=poll_id,
            world_state=self.world_state,
        )

        return {
            "accepted": True,
            "result": result,
            "world_state": self.world_state.copy(),
        }
