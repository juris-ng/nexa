from typing import Any, Dict, List

from media_models import MediaAlignment, MediaContentType, MediaReport


class RumourEngine:
    """
    Generates explicitly unverified rumours based on public events.
    """

    def generate(
        self,
        event: Dict[str, Any],
        simulation_day: int,
    ) -> List[MediaReport]:
        event_type = event.get("event_type", event.get("type", "general"))
        event_id = event.get("event_id", event.get("id"))

        rumours = [
            (
                MediaAlignment.NEUTRAL,
                "Residents are sharing unverified claims about what happened.",
            ),
            (
                MediaAlignment.UNION,
                "Some workers claim the official account leaves out key details.",
            ),
            (
                MediaAlignment.GOVERNMENT,
                "Officials warn that unverified claims may cause further tension.",
            ),
        ]

        reports: List[MediaReport] = []

        for alignment, rumour_text in rumours:
            reports.append(
                MediaReport(
                    content_type=MediaContentType.RUMOUR,
                    organization_name="Public Rumour Network",
                    alignment=alignment,
                    event_id=event_id,
                    event_type=event_type,
                    rumour=rumour_text,
                    tone="unverified",
                    bias_notes=(
                        "Rumour only. It must not be treated as confirmed world truth."
                    ),
                    visibility="public",
                    simulation_day=simulation_day,
                )
            )

        return reports
