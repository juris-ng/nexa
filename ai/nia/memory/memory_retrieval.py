import re
from typing import Dict, List, Tuple

from memory_models import Memory
from memory_store import MemoryStore


class MemoryRetrieval:
    """
    Retrieves compact, relevant, authorised memory records for NIA.
    """

    def __init__(self, memory_store: MemoryStore) -> None:
        self.memory_store = memory_store

    @staticmethod
    def _tokens(text: str) -> set[str]:
        return set(re.findall(r"[a-zA-Z0-9_]+", text.lower()))

    def _keyword_score(
        self,
        query: str,
        memory: Memory,
    ) -> float:
        query_tokens = self._tokens(query)

        searchable_text = " ".join(
            [
                memory.content,
                " ".join(memory.tags),
                " ".join(memory.subject_ids),
                memory.event_id or "",
            ]
        )

        memory_tokens = self._tokens(searchable_text)

        if not query_tokens or not memory_tokens:
            return 0.0

        overlap = len(query_tokens.intersection(memory_tokens))
        return min(100.0, (overlap / len(query_tokens)) * 100.0)

    def score_memory(
        self,
        query: str,
        memory: Memory,
    ) -> Tuple[float, Dict[str, float]]:
        keyword = self._keyword_score(query, memory)
        recency = memory.calculate_recency()

        score = (
            keyword * 0.35
            + memory.importance * 0.25
            + memory.emotional_weight * 0.10
            + recency * 0.15
            + memory.relationship * 0.10
            - memory.secrecy * 0.05
        )

        details = {
            "keyword": round(keyword, 2),
            "importance": memory.importance,
            "emotional_weight": memory.emotional_weight,
            "recency": recency,
            "relationship": memory.relationship,
            "secrecy": memory.secrecy,
        }

        return round(max(0.0, score), 2), details

    def retrieve(
        self,
        query: str,
        requester: str = "NIA",
        clearance: float = 0.0,
        limit: int = 5,
    ) -> List[Dict[str, object]]:
        ranked: List[Dict[str, object]] = []

        for memory in self.memory_store.all():
            if not memory.is_authorised_for(requester, clearance):
                continue

            score, score_details = self.score_memory(query, memory)

            if score <= 0:
                continue

            ranked.append(
                {
                    "memory": memory,
                    "score": score,
                    "score_details": score_details,
                }
            )

        ranked.sort(key=lambda item: item["score"], reverse=True)
        return ranked[:limit]
