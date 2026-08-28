from director_models import DirectorMetrics, WorldObservation


class TensionAnalyzer:
    """
    Calculates tension, pacing and entertainment-relevant state
    using deterministic NEXA world signals.
    """

    @staticmethod
    def clamp(value: float) -> float:
        return max(0.0, min(100.0, round(value, 2)))

    def analyse(self, observation: WorldObservation) -> DirectorMetrics:
        state = observation.world_state

        union_anger = float(state.get("union_anger", 0.0))
        unemployment = float(state.get("unemployment_rate", 0.0))
        approval = float(state.get("mayor_approval", 50.0))
        crime = float(state.get("crime_rate", 0.0))

        audience_commands = float(
            observation.audience_activity.get("commands_last_hour", 0)
        )
        audience_votes = float(
            observation.audience_activity.get("votes_last_hour", 0)
        )
        player_actions = float(
            observation.player_activity.get("actions_last_hour", 0)
        )

        active_mystery_count = len(observation.active_mysteries)
        recent_event_count = len(observation.recent_events)

        labour_pressure = (
            union_anger * 0.45
            + min(unemployment * 4.0, 100.0) * 0.30
            + (100.0 - approval) * 0.25
        )

        social_pressure = crime * 0.35 + (100.0 - approval) * 0.20

        tension = self.clamp(
            labour_pressure * 0.60
            + social_pressure * 0.40
        )

        engagement = self.clamp(
            audience_commands * 6.0
            + audience_votes * 3.0
            + player_actions * 5.0
        )

        mystery_potential = self.clamp(
            active_mystery_count * 18.0
            + recent_event_count * 7.0
            + tension * 0.25
        )

        novelty = self.clamp(
            75.0 - recent_event_count * 8.0 + active_mystery_count * 5.0
        )

        importance = self.clamp(
            tension * 0.55
            + mystery_potential * 0.25
            + engagement * 0.20
        )

        interest = self.clamp(
            tension * 0.30
            + engagement * 0.30
            + mystery_potential * 0.25
            + novelty * 0.15
        )

        pacing = self.clamp(
            recent_event_count * 15.0
            + audience_commands * 4.0
            + active_mystery_count * 10.0
        )

        return DirectorMetrics(
            interest=interest,
            tension=tension,
            novelty=novelty,
            importance=importance,
            mystery_potential=mystery_potential,
            audience_engagement=engagement,
            pacing=pacing,
        )

    @staticmethod
    def protest_pressure_rule(observation: WorldObservation) -> bool:
        state = observation.world_state

        return (
            float(state.get("union_anger", 0.0)) > 80.0
            and float(state.get("unemployment_rate", 0.0)) > 15.0
            and float(state.get("mayor_approval", 50.0)) < 30.0
        )
