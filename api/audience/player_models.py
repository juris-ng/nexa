from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List
import uuid


@dataclass
class PlayerProfile:
    """
    NEXA audience player profile.
    """

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "Anonymous Viewer"
    reputation: float = 50.0
    wealth: float = 0.0
    influence: float = 0.0
    relationships: Dict[str, Dict[str, float]] = field(
        default_factory=dict
    )
    faction_alignment: Dict[str, float] = field(
        default_factory=dict
    )
    history: List[Dict[str, Any]] = field(default_factory=list)
    actions: List[Dict[str, Any]] = field(default_factory=list)
    achievements: List[str] = field(default_factory=list)
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    @staticmethod
    def clamp(value: float) -> float:
        return max(0.0, min(100.0, round(value, 2)))

    def record_action(
        self,
        action: Dict[str, Any],
    ) -> None:
        self.actions.append(action)
        self.history.append(action)
        self.updated_at = datetime.now(timezone.utc)

    def change_reputation(self, change: float) -> None:
        self.reputation = self.clamp(self.reputation + change)
        self.updated_at = datetime.now(timezone.utc)

    def change_influence(self, change: float) -> None:
        self.influence = self.clamp(self.influence + change)
        self.updated_at = datetime.now(timezone.utc)

    def add_achievement(self, achievement: str) -> None:
        if achievement not in self.achievements:
            self.achievements.append(achievement)
            self.updated_at = datetime.now(timezone.utc)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "reputation": self.reputation,
            "wealth": self.wealth,
            "influence": self.influence,
            "relationships": self.relationships,
            "faction_alignment": self.faction_alignment,
            "history": self.history,
            "actions": self.actions,
            "achievements": self.achievements,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
