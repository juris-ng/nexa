from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from voting_models import AudiencePoll, PollOption, PollStatus


class VotingService:
    """
    Manages audience polls and validated policy consequences.
    """

    def __init__(self) -> None:
        self.polls: Dict[str, AudiencePoll] = {}

    def create_poll(
        self,
        question: str,
        options: List[PollOption],
        duration_minutes: int = 10,
    ) -> AudiencePoll:
        poll = AudiencePoll(
            question=question,
            options=options,
            deadline=(
                datetime.now(timezone.utc)
                + timedelta(minutes=duration_minutes)
            ),
        )

        self.polls[poll.id] = poll
        return poll

    def vote(
        self,
        poll_id: str,
        player_id: str,
        option_id: str,
    ) -> tuple[bool, str]:
        poll = self.polls.get(poll_id)

        if poll is None:
            return False, "Poll not found."

        if not poll.is_open():
            return False, "This poll is closed."

        option = poll.get_option(option_id)

        if option is None:
            return False, "Poll option not found."

        previous_option_id = poll.votes_by_player.get(player_id)

        if previous_option_id is not None:
            previous_option = poll.get_option(previous_option_id)

            if previous_option is not None:
                previous_option.votes = max(0, previous_option.votes - 1)

        option.votes += 1
        poll.votes_by_player[player_id] = option_id

        return True, "Vote recorded."

    def close_poll(
        self,
        poll_id: str,
    ) -> Optional[PollOption]:
        poll = self.polls.get(poll_id)

        if poll is None:
            return None

        if poll.status == PollStatus.OPEN:
            poll.status = PollStatus.CLOSED

        if not poll.options:
            return None

        winner = max(
            poll.options,
            key=lambda option: option.votes,
        )

        poll.result_option_id = winner.id
        return winner

    def execute_result(
        self,
        poll_id: str,
        world_state: Dict[str, Any],
    ) -> Dict[str, Any]:
        poll = self.polls.get(poll_id)

        if poll is None:
            raise KeyError("Poll not found.")

        if poll.status == PollStatus.OPEN:
            raise ValueError(
                "Poll must be closed before its result can be executed."
            )

        if poll.result_option_id is None:
            raise ValueError("Poll has no result.")

        winning_option = poll.get_option(poll.result_option_id)

        if winning_option is None:
            raise ValueError("Winning option not found.")

        consequence = winning_option.consequence

        allowed_keys = {
            "tax_rate_change",
            "mayor_approval_change",
            "union_anger_change",
            "public_interest_change",
        }

        applied_changes: Dict[str, Any] = {}

        for key, change in consequence.items():
            if key not in allowed_keys:
                continue

            if key == "tax_rate_change":
                current = float(world_state.get("tax_rate", 20.0))
                world_state["tax_rate"] = max(
                    0.0,
                    min(100.0, current + float(change)),
                )
                applied_changes["tax_rate"] = world_state["tax_rate"]

            elif key == "mayor_approval_change":
                current = float(
                    world_state.get("mayor_approval", 50.0)
                )
                world_state["mayor_approval"] = max(
                    0.0,
                    min(100.0, current + float(change)),
                )
                applied_changes["mayor_approval"] = (
                    world_state["mayor_approval"]
                )

            elif key == "union_anger_change":
                current = float(world_state.get("union_anger", 50.0))
                world_state["union_anger"] = max(
                    0.0,
                    min(100.0, current + float(change)),
                )
                applied_changes["union_anger"] = world_state["union_anger"]

            elif key == "public_interest_change":
                current = float(
                    world_state.get("public_interest", 50.0)
                )
                world_state["public_interest"] = max(
                    0.0,
                    min(100.0, current + float(change)),
                )
                applied_changes["public_interest"] = (
                    world_state["public_interest"]
                )

        poll.status = PollStatus.EXECUTED

        return {
            "poll_id": poll.id,
            "question": poll.question,
            "winning_option": winning_option.to_dict(),
            "applied_world_changes": applied_changes,
        }
