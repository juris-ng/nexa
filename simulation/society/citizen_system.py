from dataclasses import dataclass, field
from typing import Dict, List, Optional
import uuid

from needs_system import NeedsSystem
from motivation_system import MotivationSystem


@dataclass
class Citizen:
    """
    Represents a meaningful simulated NEXA citizen.
    """

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "Unnamed Citizen"
    age: int = 30
    occupation: str = "Unemployed"
    faction_id: Optional[str] = None
    location_id: Optional[str] = None
    wealth: float = 0.0
    reputation: float = 50.0
    employed: bool = False
    has_home: bool = True
    needs: Dict[str, float] = field(
        default_factory=NeedsSystem.default_needs
    )
    motivations: Dict[str, float] = field(
        default_factory=MotivationSystem.default_motivations
    )
    goals: List[str] = field(default_factory=list)
    fears: List[str] = field(default_factory=list)
    beliefs: List[str] = field(default_factory=list)
    current_activity: str = "idle"

    def to_dict(self) -> Dict[str, object]:
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "occupation": self.occupation,
            "faction_id": self.faction_id,
            "location_id": self.location_id,
            "wealth": self.wealth,
            "reputation": self.reputation,
            "employed": self.employed,
            "has_home": self.has_home,
            "needs": self.needs,
            "motivations": self.motivations,
            "goals": self.goals,
            "fears": self.fears,
            "beliefs": self.beliefs,
            "current_activity": self.current_activity,
        }


class CitizenSystem:
    """
    Creates citizens and chooses their next behaviour from their state.
    """

    def __init__(self) -> None:
        self.needs_system = NeedsSystem()
        self.motivation_system = MotivationSystem()
        self.citizens: Dict[str, Citizen] = {}

    def add_citizen(self, citizen: Citizen) -> Citizen:
        self.citizens[citizen.id] = citizen
        return citizen

    def create_citizen(
        self,
        name: str,
        age: int,
        occupation: str,
        faction_id: Optional[str] = None,
        employed: bool = False,
        has_home: bool = True,
    ) -> Citizen:
        citizen = Citizen(
            name=name,
            age=age,
            occupation=occupation,
            faction_id=faction_id,
            employed=employed,
            has_home=has_home,
        )
        return self.add_citizen(citizen)

    def update_citizen(
        self,
        citizen: Citizen,
        crime_pressure: float,
        social_support: float,
        political_pressure: float,
        resentment: float,
    ) -> Citizen:
        citizen.needs = self.needs_system.update_needs(
            needs=citizen.needs,
            employed=citizen.employed,
            has_home=citizen.has_home,
            crime_pressure=crime_pressure,
            social_support=social_support,
        )

        citizen.motivations = self.motivation_system.update_motivations(
            motivations=citizen.motivations,
            needs=citizen.needs,
            resentment=resentment,
            political_pressure=political_pressure,
        )

        citizen.current_activity = self.choose_activity(
            citizen=citizen,
            resentment=resentment,
            political_pressure=political_pressure,
        )

        return citizen

    def choose_activity(
        self,
        citizen: Citizen,
        resentment: float,
        political_pressure: float,
    ) -> str:
        urgent_need = self.needs_system.most_urgent_need(citizen.needs)
        dominant_motivation = self.motivation_system.dominant_motivation(
            citizen.motivations
        )

        if citizen.needs["food"] < 25:
            return "searching_for_food"

        if citizen.needs["shelter"] < 25:
            return "seeking_shelter"

        if citizen.needs["safety"] < 25:
            return "avoiding_danger"

        if citizen.needs["money"] < 25:
            return "searching_for_income"

        if (
            resentment > 70
            and citizen.motivations["revenge"] > 60
        ):
            return "confronting_rival"

        if (
            political_pressure > 70
            and citizen.motivations["freedom"] > 60
        ):
            return "considering_protest"

        if citizen.employed:
            return "working"

        if dominant_motivation == "wealth":
            return "seeking_work"

        if dominant_motivation == "love":
            return "seeking_social_connection"

        if dominant_motivation == "recognition":
            return "pursuing_recognition"

        if dominant_motivation == "ideology":
            return "engaging_with_faction"

        return "pursuing_personal_goal"

    def get_citizen(self, citizen_id: str) -> Citizen | None:
        return self.citizens.get(citizen_id)

    def get_all_citizens(self) -> List[Citizen]:
        return list(self.citizens.values())
