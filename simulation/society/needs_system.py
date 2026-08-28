from typing import Dict


class NeedsSystem:
    """
    Controls core citizen needs.

    Each value ranges from 0 to 100:
    0 means the need is critically unmet.
    100 means the need is fully satisfied.
    """

    NEED_KEYS = (
        "money",
        "food",
        "shelter",
        "safety",
        "social_connection",
        "status",
        "purpose",
    )

    @classmethod
    def default_needs(cls) -> Dict[str, float]:
        return {
            "money": 60.0,
            "food": 70.0,
            "shelter": 75.0,
            "safety": 70.0,
            "social_connection": 60.0,
            "status": 50.0,
            "purpose": 55.0,
        }

    @staticmethod
    def clamp(value: float) -> float:
        return max(0.0, min(100.0, round(value, 2)))

    def update_needs(
        self,
        needs: Dict[str, float],
        employed: bool,
        has_home: bool,
        crime_pressure: float,
        social_support: float,
    ) -> Dict[str, float]:
        updated = needs.copy()

        updated["food"] = self.clamp(updated["food"] - 0.40)
        updated["social_connection"] = self.clamp(
            updated["social_connection"] - 0.10 + social_support * 0.05
        )
        updated["safety"] = self.clamp(
            updated["safety"] - crime_pressure * 0.03
        )
        updated["status"] = self.clamp(updated["status"] - 0.05)
        updated["purpose"] = self.clamp(updated["purpose"] - 0.05)

        if employed:
            updated["money"] = self.clamp(updated["money"] + 0.30)
            updated["purpose"] = self.clamp(updated["purpose"] + 0.15)
            updated["status"] = self.clamp(updated["status"] + 0.05)
        else:
            updated["money"] = self.clamp(updated["money"] - 0.35)
            updated["purpose"] = self.clamp(updated["purpose"] - 0.20)

        if has_home:
            updated["shelter"] = self.clamp(updated["shelter"] + 0.10)
        else:
            updated["shelter"] = self.clamp(updated["shelter"] - 0.50)
            updated["safety"] = self.clamp(updated["safety"] - 0.20)

        return updated

    @staticmethod
    def most_urgent_need(needs: Dict[str, float]) -> str:
        return min(needs, key=needs.get)
