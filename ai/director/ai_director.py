from typing import Any, Dict, List

from director_models import EventProposal
from world_observer import WorldObserver
from tension_analyzer import TensionAnalyzer
from possibility_generator import PossibilityGenerator
from event_scorer import EventScorer
from director_scheduler import DirectorScheduler


class AIDirector:
    """
    NEXA AI Director.

    Loop:
    OBSERVE -> ANALYSE -> GENERATE -> RANK -> SELECT
    -> SCHEDULE -> MONITOR -> ADAPT

    It proposes possibilities only. NEXA simulation and event systems
    retain authority over validation and execution.
    """

    def __init__(self) -> None:
        self.observer = WorldObserver()
        self.analyzer = TensionAnalyzer()
        self.generator = PossibilityGenerator()
        self.scorer = EventScorer()
        self.scheduler = DirectorScheduler()
        self.last_metrics: Dict[str, float] = {}

    def run_cycle(
        self,
        world_state: Dict[str, Any],
        player_activity: Dict[str, Any] | None = None,
        audience_activity: Dict[str, Any] | None = None,
        active_mysteries: List[Dict[str, Any]] | None = None,
        recent_events: List[Dict[str, Any]] | None = None,
        nia_activity: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        observation = self.observer.observe(
            world_state=world_state,
            player_activity=player_activity,
            audience_activity=audience_activity,
            active_mysteries=active_mysteries,
            recent_events=recent_events,
            nia_activity=nia_activity,
        )

        metrics = self.analyzer.analyse(observation)
        proposals = self.generator.generate(observation, metrics)
        ranked_proposals = self.scorer.rank(
            proposals,
            metrics,
            observation,
        )

        selected = self.scheduler.schedule(ranked_proposals)
        self.last_metrics = metrics.to_dict()

        return {
            "observation_time": observation.observed_at.isoformat(),
            "metrics": metrics.to_dict(),
            "generated_proposals": [
                proposal.to_dict()
                for proposal in proposals
            ],
            "ranked_proposals": [
                proposal.to_dict()
                for proposal in ranked_proposals
            ],
            "selected_proposal": (
                selected.to_dict()
                if selected
                else None
            ),
            "scheduled_proposals": [
                proposal.to_dict()
                for proposal in self.scheduler.get_scheduled()
            ],
        }

    def get_last_metrics(self) -> Dict[str, float]:
        return self.last_metrics.copy()

    def get_scheduled_proposals(self) -> List[EventProposal]:
        return self.scheduler.get_scheduled()
