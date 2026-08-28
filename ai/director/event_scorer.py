from typing import List

from director_models import DirectorMetrics, EventProposal, WorldObservation


class EventScorer:
    """
    Ranks valid Director proposals using interest, tension, novelty,
    importance, mystery potential and audience engagement.
    """

    @staticmethod
    def clamp(value: float) -> float:
        return max(0.0, min(100.0, round(value, 2)))

    def score(
        self,
        proposal: EventProposal,
        metrics: DirectorMetrics,
        observation: WorldObservation,
    ) -> float:
        event_bonus = {
            "protest": 22.0,
            "political_response": 14.0,
            "mystery_lead": 16.0,
            "social_development": 8.0,
        }.get(proposal.event_type, 5.0)

        faction_bonus = min(
            15.0,
            len(proposal.related_factions) * 4.0,
        )

        mystery_bonus = min(
            15.0,
            len(proposal.related_mysteries) * 6.0,
        )

        score = (
            metrics.interest * 0.25
            + metrics.tension * 0.20
            + metrics.novelty * 0.10
            + metrics.importance * 0.15
            + metrics.mystery_potential * 0.15
            + metrics.audience_engagement * 0.15
            + event_bonus
            + faction_bonus
            + mystery_bonus
        )

        proposal.priority = self.clamp(score)
        return proposal.priority

    def rank(
        self,
        proposals: List[EventProposal],
        metrics: DirectorMetrics,
        observation: WorldObservation,
    ) -> List[EventProposal]:
        for proposal in proposals:
            self.score(proposal, metrics, observation)

        return sorted(
            proposals,
            key=lambda proposal: proposal.priority,
            reverse=True,
        )
