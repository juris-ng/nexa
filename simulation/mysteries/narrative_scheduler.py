from typing import List

from mystery_models import Mystery, StoryBeat


class NarrativeScheduler:
    """
    Identifies delayed mystery story beats that are eligible to run.
    """

    def get_due_beats(
        self,
        mystery: Mystery,
        simulation_day: int,
        audience_connected_clues: bool = False,
    ) -> List[StoryBeat]:
        due_beats: List[StoryBeat] = []

        for beat in mystery.story_beats:
            if beat.executed:
                continue

            if simulation_day < beat.simulation_day:
                continue

            if (
                beat.audience_required
                and not audience_connected_clues
            ):
                continue

            due_beats.append(beat)

        return due_beats
