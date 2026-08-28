from typing import Any, Dict, List

from media_models import MediaAlignment, MediaContentType, MediaReport


class SocialReactionEngine:
    """
    Produces aggregate social responses, not individual user posts.
    """

    def generate(
        self,
        event: Dict[str, Any],
        simulation_day: int,
    ) -> List[MediaReport]:
        event_type = event.get("event_type", event.get("type", "general"))
        event_id = event.get("event_id", event.get("id"))

        reactions = [
            (
                MediaAlignment.NEUTRAL,
                "Public discussion is rising as citizens seek clearer information.",
            ),
            (
                MediaAlignment.UNION,
                "Worker networks are calling for solidarity and further action.",
            ),
            (
                MediaAlignment.GOVERNMENT,
                "Civic channels are urging calm and compliance with safety guidance.",
            ),
            (
                MediaAlignment.CORPORATE,
                "Business groups are monitoring the event's economic impact.",
            ),
        ]

        reports: List[MediaReport] = []

        for alignment, reaction in reactions:
            reports.append(
                MediaReport(
                    content_type=MediaContentType.SOCIAL_REACTION,
                    organization_name="NEXA Public Network",
                    alignment=alignment,
                    event_id=event_id,
                    event_type=event_type,
                    social_reaction=reaction,
                    tone="public reaction",
                    bias_notes=(
                        "Aggregate fictional social reaction generated from event context."
                    ),
                    visibility="public",
                    simulation_day=simulation_day,
                )
            )

        return reports
