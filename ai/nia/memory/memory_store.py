import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from memory_models import Memory, MemoryType


class MemoryStore:
    """
    Persistent local store for NIA memory records.

    JSON is the Phase 8 persistence layer.
    PostgreSQL integration will replace or complement this later.
    """

    def __init__(self, storage_file: Optional[Path] = None) -> None:
        default_path = Path(__file__).parent / "nia_memories.json"
        self.storage_file = storage_file or default_path
        self.memories: Dict[str, Memory] = {}
        self.load()

    @staticmethod
    def _parse_datetime(value: str) -> datetime:
        parsed = datetime.fromisoformat(value)

        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=timezone.utc)

        return parsed

    def load(self) -> None:
        if not self.storage_file.exists():
            return

        try:
            records = json.loads(
                self.storage_file.read_text(encoding="utf-8")
            )
        except (json.JSONDecodeError, OSError):
            return

        for record in records:
            memory = Memory(
                id=record["id"],
                memory_type=MemoryType(record["memory_type"]),
                content=record["content"],
                subject_ids=record.get("subject_ids", []),
                event_id=record.get("event_id"),
                importance=record.get("importance", 50.0),
                emotional_weight=record.get("emotional_weight", 50.0),
                relationship=record.get("relationship", 50.0),
                secrecy=record.get("secrecy", 0.0),
                allowed_audience=record.get("allowed_audience", ["NIA"]),
                tags=record.get("tags", []),
                metadata=record.get("metadata", {}),
                created_at=self._parse_datetime(record["created_at"]),
                updated_at=self._parse_datetime(record["updated_at"]),
            )
            self.memories[memory.id] = memory

    def save(self) -> None:
        records = [
            memory.to_dict(include_content=True)
            for memory in self.memories.values()
        ]

        self.storage_file.write_text(
            json.dumps(records, indent=2),
            encoding="utf-8",
        )

    def add(self, memory: Memory) -> Memory:
        memory.importance = Memory.clamp(memory.importance)
        memory.emotional_weight = Memory.clamp(memory.emotional_weight)
        memory.relationship = Memory.clamp(memory.relationship)
        memory.secrecy = Memory.clamp(memory.secrecy)
        memory.updated_at = datetime.now(timezone.utc)

        self.memories[memory.id] = memory
        self.save()
        return memory

    def get(self, memory_id: str) -> Optional[Memory]:
        return self.memories.get(memory_id)

    def all(self) -> List[Memory]:
        return list(self.memories.values())

    def update(self, memory: Memory) -> Memory:
        if memory.id not in self.memories:
            raise KeyError(f"Memory not found: {memory.id}")

        memory.updated_at = datetime.now(timezone.utc)
        self.memories[memory.id] = memory
        self.save()
        return memory

    def delete(self, memory_id: str) -> bool:
        if memory_id not in self.memories:
            return False

        del self.memories[memory_id]
        self.save()
        return True
