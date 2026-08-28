from typing import Dict, Optional

from memory_models import Memory, MemoryType
from memory_store import MemoryStore


class RelationshipMemory:
    """
    Stores NIA's long-term relationship impressions of characters.
    """

    def __init__(self, memory_store: MemoryStore) -> None:
        self.memory_store = memory_store

    def remember_character(
        self,
        character_id: str,
        character_name: str,
        impression: str,
        trust: float,
        affection: float,
        fear: float,
        respect: float,
        resentment: float,
        secrecy: float = 0.0,
    ) -> Memory:
        relationship_score = max(
            0.0,
            min(
                100.0,
                (trust + affection + respect - fear - resentment) / 3,
            ),
        )

        content = (
            f"NIA's relationship memory of {character_name}: {impression}. "
            f"Trust={trust}, affection={affection}, fear={fear}, "
            f"respect={respect}, resentment={resentment}."
        )

        memory = Memory(
            memory_type=MemoryType.RELATIONSHIP,
            content=content,
            subject_ids=[character_id],
            importance=70.0,
            emotional_weight=max(affection, fear, resentment),
            relationship=relationship_score,
            secrecy=secrecy,
            allowed_audience=["NIA"],
            tags=[
                "relationship",
                character_name.lower(),
                character_id,
            ],
            metadata={
                "character_name": character_name,
                "trust": trust,
                "affection": affection,
                "fear": fear,
                "respect": respect,
                "resentment": resentment,
            },
        )

        return self.memory_store.add(memory)

    def get_latest_for_character(
        self,
        character_id: str,
    ) -> Optional[Memory]:
        records = [
            memory
            for memory in self.memory_store.all()
            if memory.memory_type == MemoryType.RELATIONSHIP
            and character_id in memory.subject_ids
        ]

        if not records:
            return None

        return max(records, key=lambda memory: memory.updated_at)
