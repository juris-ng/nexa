from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid


class MediaAlignment(str, Enum):
    GOVERNMENT = "government"
    INDEPENDENT = "independent"
    UNION = "union"
    CORPORATE = "corporate"
    NEUTRAL = "neutral"


class MediaContentType(str, Enum):
    HEADLINE = "headline"
    ARTICLE = "article"
    BROADCAST = "broadcast"
    RUMOUR = "rumour"
    SOCIAL_REACTION = "social_reaction"


@dataclass
class MediaOrganization:
    """
    A fictional NEXA media organisation.
    """

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "Unnamed Media"
    alignment: MediaAlignment = MediaAlignment.NEUTRAL
    credibility: float = 50.0
    influence: float = 50.0
    audience_description: str = ""
    editorial_position: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "alignment": self.alignment.value,
            "credibility": self.credibility,
            "influence": self.influence,
            "audience_description": self.audience_description,
            "editorial_position": self.editorial_position,
        }


@dataclass
class MediaReport:
    """
    A news item, broadcast, rumour or public reaction.
    """

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    content_type: MediaContentType = MediaContentType.HEADLINE
    organization_id: Optional[str] = None
    organization_name: str = ""
    alignment: MediaAlignment = MediaAlignment.NEUTRAL
    event_id: Optional[str] = None
    event_type: str = ""
    headline: str = ""
    article: str = ""
    broadcast: str = ""
    rumour: str = ""
    social_reaction: str = ""
    tone: str = "neutral"
    bias_notes: str = ""
    visibility: str = "public"
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    simulation_day: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "content_type": self.content_type.value,
            "organization_id": self.organization_id,
            "organization_name": self.organization_name,
            "alignment": self.alignment.value,
            "event_id": self.event_id,
            "event_type": self.event_type,
            "headline": self.headline,
            "article": self.article,
            "broadcast": self.broadcast,
            "rumour": self.rumour,
            "social_reaction": self.social_reaction,
            "tone": self.tone,
            "bias_notes": self.bias_notes,
            "visibility": self.visibility,
            "created_at": self.created_at.isoformat(),
            "simulation_day": self.simulation_day,
        }
