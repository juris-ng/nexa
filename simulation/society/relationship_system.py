from dataclasses import dataclass, field
from typing import Dict, List


RELATIONSHIP_TYPES = {
    "friend",
    "enemy",
    "family",
    "employer",
    "employee",
    "ally",
    "rival",
    "romantic",
    "political",
}


@dataclass
class Relationship:
    source_character_id: str
    target_character_id: str
    relationship_type: str
    trust: float = 50.0
    affection: float = 50.0
    fear: float = 0.0
    respect: float = 50.0
    resentment: float = 0.0

    def to_dict(self) -> Dict[str, float | str]:
        return {
            "source_character_id": self.source_character_id,
            "target_character_id": self.target_character_id,
            "relationship_type": self.relationship_type,
            "trust": self.trust,
            "affection": self.affection,
            "fear": self.fear,
            "respect": self.respect,
            "resentment": self.resentment,
        }


class RelationshipSystem:
    """
    Stores and updates relationships between citizens.
    """

    def __init__(self) -> None:
        self.relationships: Dict[str, List[Relationship]] = {}

    @staticmethod
    def clamp(value: float) -> float:
        return max(0.0, min(100.0, round(value, 2)))

    def add_relationship(
        self,
        source_character_id: str,
        target_character_id: str,
        relationship_type: str,
        trust: float = 50.0,
        affection: float = 50.0,
        fear: float = 0.0,
        respect: float = 50.0,
        resentment: float = 0.0,
    ) -> Relationship:
        if relationship_type not in RELATIONSHIP_TYPES:
            raise ValueError(
                f"Invalid relationship type: {relationship_type}"
            )

        relationship = Relationship(
            source_character_id=source_character_id,
            target_character_id=target_character_id,
            relationship_type=relationship_type,
            trust=self.clamp(trust),
            affection=self.clamp(affection),
            fear=self.clamp(fear),
            respect=self.clamp(respect),
            resentment=self.clamp(resentment),
        )

        self.relationships.setdefault(source_character_id, []).append(
            relationship
        )
        return relationship

    def get_relationships(
        self,
        character_id: str,
    ) -> List[Relationship]:
        return self.relationships.get(character_id, [])

    def get_average_social_support(self, character_id: str) -> float:
        relationships = self.get_relationships(character_id)

        if not relationships:
            return 0.0

        support_scores = []

        for relationship in relationships:
            score = (
                relationship.trust
                + relationship.affection
                + relationship.respect
                - relationship.fear
                - relationship.resentment
            ) / 3

            support_scores.append(self.clamp(score))

        return round(sum(support_scores) / len(support_scores), 2)

    def get_average_resentment(self, character_id: str) -> float:
        relationships = self.get_relationships(character_id)

        if not relationships:
            return 0.0

        total = sum(item.resentment for item in relationships)
        return round(total / len(relationships), 2)

    def change_relationship(
        self,
        source_character_id: str,
        target_character_id: str,
        changes: Dict[str, float],
    ) -> Relationship | None:
        for relationship in self.get_relationships(source_character_id):
            if relationship.target_character_id == target_character_id:
                for field_name, change in changes.items():
                    if hasattr(relationship, field_name):
                        current_value = getattr(relationship, field_name)
                        setattr(
                            relationship,
                            field_name,
                            self.clamp(current_value + change),
                        )
                return relationship

        return None
