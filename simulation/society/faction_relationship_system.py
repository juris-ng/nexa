from typing import Dict, Tuple


class FactionRelationshipSystem:
    """
    Tracks dynamic relations between factions.

    Values range from -100 to +100:
    -100 = total hostility
       0 = neutral
    +100 = total alliance
    """

    def __init__(self) -> None:
        self.relationships: Dict[Tuple[str, str], float] = {}

    @staticmethod
    def clamp(value: float) -> float:
        return max(-100.0, min(100.0, round(value, 2)))

    @staticmethod
    def _key(faction_a_id: str, faction_b_id: str) -> Tuple[str, str]:
        return tuple(sorted((faction_a_id, faction_b_id)))

    def set_relationship(
        self,
        faction_a_id: str,
        faction_b_id: str,
        value: float,
    ) -> None:
        self.relationships[self._key(faction_a_id, faction_b_id)] = (
            self.clamp(value)
        )

    def get_relationship(
        self,
        faction_a_id: str,
        faction_b_id: str,
    ) -> float:
        return self.relationships.get(
            self._key(faction_a_id, faction_b_id),
            0.0,
        )

    def change_relationship(
        self,
        faction_a_id: str,
        faction_b_id: str,
        change: float,
    ) -> float:
        current = self.get_relationship(faction_a_id, faction_b_id)
        updated = self.clamp(current + change)

        self.set_relationship(faction_a_id, faction_b_id, updated)
        return updated

    def seed_default_relationships(self) -> None:
        self.set_relationship("government", "union", -63.0)
        self.set_relationship("corporation", "government", 71.0)
        self.set_relationship("criminal_faction", "police", -88.0)

    def get_all_relationships(self) -> Dict[str, float]:
        return {
            f"{faction_a} <-> {faction_b}": value
            for (faction_a, faction_b), value in self.relationships.items()
        }
