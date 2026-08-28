from datetime import datetime
from typing import Dict, List

from citizen_system import Citizen, CitizenSystem
from relationship_system import RelationshipSystem
from faction_relationship_system import FactionRelationshipSystem


class SocietyEngine:
    """
    NEXA Society Engine.

    Coordinates citizens, individual relationships,
    faction relations, needs, motivations and behaviour.
    """

    def __init__(self) -> None:
        self.citizen_system = CitizenSystem()
        self.relationship_system = RelationshipSystem()
        self.faction_relationship_system = FactionRelationshipSystem()
        self.faction_relationship_system.seed_default_relationships()

    def create_citizen(
        self,
        name: str,
        age: int,
        occupation: str,
        faction_id: str | None = None,
        employed: bool = False,
        has_home: bool = True,
    ) -> Citizen:
        return self.citizen_system.create_citizen(
            name=name,
            age=age,
            occupation=occupation,
            faction_id=faction_id,
            employed=employed,
            has_home=has_home,
        )

    def tick(
        self,
        day: int,
        simulation_time: datetime,
        crime_pressure: float = 20.0,
        political_pressure: float = 30.0,
    ) -> None:
        for citizen in self.citizen_system.get_all_citizens():
            social_support = self.relationship_system.get_average_social_support(
                citizen.id
            )
            resentment = self.relationship_system.get_average_resentment(
                citizen.id
            )

            self.citizen_system.update_citizen(
                citizen=citizen,
                crime_pressure=crime_pressure,
                social_support=social_support,
                political_pressure=political_pressure,
                resentment=resentment,
            )

    def get_state(self) -> Dict[str, object]:
        citizens = self.citizen_system.get_all_citizens()

        activities: Dict[str, int] = {}
        for citizen in citizens:
            activities[citizen.current_activity] = (
                activities.get(citizen.current_activity, 0) + 1
            )

        return {
            "citizen_count": len(citizens),
            "activities": activities,
            "faction_relationships": (
                self.faction_relationship_system.get_all_relationships()
            ),
            "citizens": [citizen.to_dict() for citizen in citizens],
        }

    def get_citizens(self) -> List[Citizen]:
        return self.citizen_system.get_all_citizens()
