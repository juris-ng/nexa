from typing import Any, Dict, List, Optional

from conversation_memory import ConversationMemory
from memory_models import Memory, MemoryType
from memory_retrieval import MemoryRetrieval
from memory_store import MemoryStore
from relationship_memory import RelationshipMemory


class MemoryService:
    """
    Central NIA memory service.

    Memory flow:
    User question -> retrieve relevant authorised memories
    -> combine with world context -> NIA response.
    """

    def __init__(self) -> None:
        self.store = MemoryStore()
        self.retrieval = MemoryRetrieval(self.store)
        self.conversation = ConversationMemory()
        self.relationships = RelationshipMemory(self.store)

    def remember_episodic(
        self,
        content: str,
        event_id: Optional[str] = None,
        subject_ids: Optional[List[str]] = None,
        importance: float = 50.0,
        emotional_weight: float = 50.0,
        relationship: float = 50.0,
        secrecy: float = 0.0,
        tags: Optional[List[str]] = None,
    ) -> Memory:
        memory = Memory(
            memory_type=MemoryType.EPISODIC,
            content=content,
            event_id=event_id,
            subject_ids=subject_ids or [],
            importance=importance,
            emotional_weight=emotional_weight,
            relationship=relationship,
            secrecy=secrecy,
            allowed_audience=["NIA"],
            tags=tags or [],
        )

        return self.store.add(memory)

    def remember_semantic(
        self,
        content: str,
        tags: Optional[List[str]] = None,
        importance: float = 60.0,
        secrecy: float = 0.0,
    ) -> Memory:
        memory = Memory(
            memory_type=MemoryType.SEMANTIC,
            content=content,
            importance=importance,
            emotional_weight=20.0,
            relationship=40.0,
            secrecy=secrecy,
            allowed_audience=["NIA"],
            tags=tags or [],
        )

        return self.store.add(memory)

    def remember_secret(
        self,
        content: str,
        subject_ids: Optional[List[str]] = None,
        secrecy: float = 80.0,
        importance: float = 70.0,
        tags: Optional[List[str]] = None,
    ) -> Memory:
        memory = Memory(
            memory_type=MemoryType.SECRET,
            content=content,
            subject_ids=subject_ids or [],
            importance=importance,
            emotional_weight=60.0,
            relationship=50.0,
            secrecy=secrecy,
            allowed_audience=["NIA"],
            tags=tags or ["secret"],
        )

        return self.store.add(memory)

    def add_conversation_message(
        self,
        speaker: str,
        content: str,
    ) -> None:
        self.conversation.add_message(speaker, content)

    def retrieve_for_nia(
        self,
        user_question: str,
        limit: int = 5,
    ) -> List[Dict[str, Any]]:
        results = self.retrieval.retrieve(
            query=user_question,
            requester="NIA",
            clearance=100.0,
            limit=limit,
        )

        return [
            {
                "memory": item["memory"].to_dict(include_content=True),
                "retrieval_score": item["score"],
                "score_details": item["score_details"],
            }
            for item in results
        ]

    def retrieve_for_user(
        self,
        user_question: str,
        player_id: str = "audience",
        clearance: float = 0.0,
        limit: int = 5,
    ) -> List[Dict[str, Any]]:
        results = self.retrieval.retrieve(
            query=user_question,
            requester=player_id,
            clearance=clearance,
            limit=limit,
        )

        return [
            {
                "memory": item["memory"].to_dict(include_content=True),
                "retrieval_score": item["score"],
                "score_details": item["score_details"],
            }
            for item in results
        ]

    def get_short_term_context(self) -> List[Dict[str, str]]:
        return self.conversation.get_recent_messages(limit=8)
