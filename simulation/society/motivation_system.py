from typing import Dict


class MotivationSystem:
    """
    Selects citizen motivations based on needs and personality scores.
    """

    MOTIVATION_KEYS = (
        "wealth",
        "power",
        "love",
        "revenge",
        "security",
        "freedom",
        "recognition",
        "ideology",
    )

    @classmethod
    def default_motivations(cls) -> Dict[str, float]:
        return {
            "wealth": 50.0,
            "power": 35.0,
            "love": 50.0,
            "revenge": 10.0,
            "security": 55.0,
            "freedom": 50.0,
            "recognition": 45.0,
            "ideology": 40.0,
        }

    @staticmethod
    def clamp(value: float) -> float:
        return max(0.0, min(100.0, round(value, 2)))

    def update_motivations(
        self,
        motivations: Dict[str, float],
        needs: Dict[str, float],
        resentment: float,
        political_pressure: float,
    ) -> Dict[str, float]:
        updated = motivations.copy()

        if needs["money"] < 40:
            updated["wealth"] = self.clamp(updated["wealth"] + 1.0)

        if needs["safety"] < 40:
            updated["security"] = self.clamp(updated["security"] + 1.0)

        if needs["social_connection"] < 40:
            updated["love"] = self.clamp(updated["love"] + 0.80)

        if needs["status"] < 40:
            updated["recognition"] = self.clamp(updated["recognition"] + 0.80)

        if needs["purpose"] < 40:
            updated["ideology"] = self.clamp(updated["ideology"] + 0.60)

        if resentment > 60:
            updated["revenge"] = self.clamp(updated["revenge"] + 1.25)

        if political_pressure > 60:
            updated["freedom"] = self.clamp(updated["freedom"] + 0.75)
            updated["ideology"] = self.clamp(updated["ideology"] + 0.75)

        return updated

    @staticmethod
    def dominant_motivation(motivations: Dict[str, float]) -> str:
        return max(motivations, key=motivations.get)
