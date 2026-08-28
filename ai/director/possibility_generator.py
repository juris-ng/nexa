from typing import List

from director_models import DirectorMetrics, EventProposal, WorldObservation
from tension_analyzer import TensionAnalyzer


class PossibilityGenerator:
    """
    Generates narrative and world-event possibilities.
    Every output remains a proposal until validated by NEXA Core.
    """

    def generate(
        self,
        observation: WorldObservation,
        metrics: DirectorMetrics,
    ) -> List[EventProposal]:
        proposals: List[EventProposal] = []

        if TensionAnalyzer.protest_pressure_rule(observation):
            proposals.append(
                EventProposal(
                    event_type="protest",
                    title="Workers Union Organises a Public Protest",
                    reason=(
                        "Union anger exceeds 80, unemployment exceeds 15%, "
                        "and mayor approval is below 30."
                    ),
                    target_location_id="city_square",
                    related_factions=["union", "government", "police"],
                    suggested_effects={
                        "protest_event_probability_increase": 40.0,
                        "requires_simulation_validation": True,
                    },
                )
            )

        if metrics.tension >= 60.0:
            proposals.append(
                EventProposal(
                    event_type="political_response",
                    title="Government Considers Emergency Labour Meeting",
                    reason=(
                        "World tension is elevated and a political response "
                        "could develop without forcing a final outcome."
                    ),
                    target_location_id="city_square",
                    related_factions=["government", "union"],
                    suggested_effects={
                        "public_attention_increase": 12.0,
                        "requires_simulation_validation": True,
                    },
                )
            )

        if metrics.mystery_potential >= 45.0:
            proposals.append(
                EventProposal(
                    event_type="mystery_lead",
                    title="New Lead Appears in an Active Mystery",
                    reason=(
                        "Active mysteries and current tension create a valid "
                        "opportunity for an evidence lead."
                    ),
                    target_location_id="eastern_warehouse",
                    related_mysteries=[
                        mystery.get("id", "unknown_mystery")
                        for mystery in observation.active_mysteries[:2]
                    ],
                    suggested_effects={
                        "evidence_lead_probability_increase": 20.0,
                        "requires_simulation_validation": True,
                    },
                )
            )

        if metrics.interest < 35.0 and metrics.pacing < 35.0:
            proposals.append(
                EventProposal(
                    event_type="social_development",
                    title="Local Community Dispute Develops",
                    reason=(
                        "The Director detected a low-interest, low-pacing "
                        "period and proposes a small valid social development."
                    ),
                    target_location_id="city_square",
                    related_factions=["government"],
                    suggested_effects={
                        "local_interest_increase": 10.0,
                        "requires_simulation_validation": True,
                    },
                )
            )

        return proposals
