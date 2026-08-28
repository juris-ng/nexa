from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from evidence_engine import EvidenceEngine
from mystery_models import (
    Evidence,
    EvidenceVisibility,
    Mystery,
    MysteryState,
    StoryBeat,
)
from narrative_scheduler import NarrativeScheduler


class MysteryEngine:
    """
    NEXA long-form mystery and narrative engine.

    Story beats remain dormant until their scheduled simulated day.
    The overall world continues operating regardless of mystery state.
    """

    def __init__(self) -> None:
        self.mysteries: Dict[str, Mystery] = {}
        self.evidence_engine = EvidenceEngine()
        self.scheduler = NarrativeScheduler()
        self.narrative_events: List[Dict[str, Any]] = []

    def add_mystery(self, mystery: Mystery) -> Mystery:
        self.mysteries[mystery.id] = mystery
        return mystery

    def get_mystery(self, mystery_id: str) -> Optional[Mystery]:
        return self.mysteries.get(mystery_id)

    def add_evidence(
        self,
        mystery_id: str,
        evidence: Evidence,
    ) -> Evidence:
        mystery = self.get_mystery(mystery_id)

        if mystery is None:
            raise KeyError(f"Mystery not found: {mystery_id}")

        self.evidence_engine.add_evidence(evidence)
        mystery.evidence_ids.append(evidence.id)
        mystery.updated_at = datetime.now(timezone.utc)

        return evidence

    def add_story_beat(
        self,
        mystery_id: str,
        story_beat: StoryBeat,
    ) -> StoryBeat:
        mystery = self.get_mystery(mystery_id)

        if mystery is None:
            raise KeyError(f"Mystery not found: {mystery_id}")

        mystery.story_beats.append(story_beat)
        mystery.updated_at = datetime.now(timezone.utc)

        return story_beat

    def process_day(
        self,
        simulation_day: int,
        audience_connected_clues: bool = False,
    ) -> List[Dict[str, Any]]:
        executed_events: List[Dict[str, Any]] = []

        for mystery in self.mysteries.values():
            due_beats = self.scheduler.get_due_beats(
                mystery=mystery,
                simulation_day=simulation_day,
                audience_connected_clues=audience_connected_clues,
            )

            for beat in due_beats:
                event = self._execute_story_beat(
                    mystery=mystery,
                    beat=beat,
                    simulation_day=simulation_day,
                )
                executed_events.append(event)

        return executed_events

    def _execute_story_beat(
        self,
        mystery: Mystery,
        beat: StoryBeat,
        simulation_day: int,
    ) -> Dict[str, Any]:
        for evidence_id in beat.reveal_evidence_ids:
            self.evidence_engine.reveal_evidence(
                evidence_id=evidence_id,
                simulation_day=simulation_day,
                visibility=EvidenceVisibility.DISCOVERED,
            )

        if beat.target_state is not None:
            mystery.state = beat.target_state

        if beat.description not in mystery.revelations:
            mystery.revelations.append(beat.description)

        mystery.updated_at = datetime.now(timezone.utc)
        beat.executed = True

        event = {
            "event_id": beat.id,
            "event_type": beat.event_type,
            "title": beat.title,
            "description": beat.description,
            "mystery_id": mystery.id,
            "mystery_title": mystery.title,
            "simulation_day": simulation_day,
            "nia_discovery": beat.nia_discovery,
            "audience_required": beat.audience_required,
            "state_after_event": mystery.state.value,
            "revealed_evidence_ids": beat.reveal_evidence_ids,
        }

        self.narrative_events.append(event)
        return event

    def get_active_mysteries(self) -> List[Dict[str, Any]]:
        return [
            mystery.to_dict()
            for mystery in self.mysteries.values()
            if mystery.state != MysteryState.RESOLVED
        ]

    def get_visible_evidence(
        self,
        mystery_id: str,
    ) -> List[Dict[str, Any]]:
        mystery = self.get_mystery(mystery_id)

        if mystery is None:
            return []

        evidence_records = self.evidence_engine.get_evidence_for_mystery(
            mystery.evidence_ids
        )

        return [
            evidence.to_dict()
            for evidence in evidence_records
            if evidence.visibility
            in (
                EvidenceVisibility.DISCOVERED,
                EvidenceVisibility.PUBLIC,
            )
        ]
