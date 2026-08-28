from typing import Any, Dict

from media_models import (
    MediaAlignment,
    MediaContentType,
    MediaOrganization,
    MediaReport,
)


class NewsGenerator:
    """
    Produces alignment-aware news coverage from the same underlying event.
    """

    def generate(
        self,
        organization: MediaOrganization,
        event: Dict[str, Any],
        simulation_day: int,
    ) -> MediaReport:
        event_type = event.get("event_type", event.get("type", "general"))
        event_id = event.get("event_id", event.get("id"))
        description = event.get(
            "description",
            event.get("cause", "An event occurred in NEXA."),
        )

        if event_type in {"protest", "police_disperse_protest"}:
            return self._generate_protest_report(
                organization=organization,
                event_id=event_id,
                event_type=event_type,
                description=description,
                simulation_day=simulation_day,
            )

        return self._generate_general_report(
            organization=organization,
            event_id=event_id,
            event_type=event_type,
            description=description,
            simulation_day=simulation_day,
        )

    def _generate_protest_report(
        self,
        organization: MediaOrganization,
        event_id: str | None,
        event_type: str,
        description: str,
        simulation_day: int,
    ) -> MediaReport:
        alignment = organization.alignment

        content = {
            MediaAlignment.GOVERNMENT: {
                "headline": "Police Restore Public Order After City Square Protest",
                "article": (
                    "Authorities say police restored public order after a protest "
                    "in City Square created serious disruption. Officials stated "
                    "that the response followed established public-safety procedures."
                ),
                "broadcast": (
                    "City Herald reports that police have restored public order "
                    "following disruption at City Square."
                ),
                "tone": "order-focused",
                "bias_notes": "Prioritises official statements and public order.",
            },
            MediaAlignment.UNION: {
                "headline": "Police Attack Peaceful Workers at City Square",
                "article": (
                    "Workers Voice reports that police dispersed peaceful workers "
                    "during a protest over economic hardship and labour conditions. "
                    "Union representatives demand accountability for the response."
                ),
                "broadcast": (
                    "Workers Voice: peaceful workers were forced from City Square "
                    "as labour anger continues to rise."
                ),
                "tone": "worker-focused",
                "bias_notes": "Prioritises worker testimony and labour rights.",
            },
            MediaAlignment.INDEPENDENT: {
                "headline": "Dozens Injured as City Square Protest Ends",
                "article": (
                    "The Independent Network reports that a protest ended after "
                    "police intervention. Multiple witnesses describe injuries, "
                    "while officials and union representatives dispute how the "
                    "confrontation began."
                ),
                "broadcast": (
                    "Independent Network: dozens were injured as the City Square "
                    "protest ended amid conflicting accounts."
                ),
                "tone": "investigative",
                "bias_notes": "Reports competing claims and highlights missing evidence.",
            },
            MediaAlignment.CORPORATE: {
                "headline": "City Square Disruption Raises Business Stability Concerns",
                "article": (
                    "Corporate Signal reports that the City Square protest disrupted "
                    "commercial activity. Business leaders call for dialogue that "
                    "protects jobs, public safety and investor confidence."
                ),
                "broadcast": (
                    "Corporate Signal: city disruption is raising concerns for "
                    "business confidence and local trade."
                ),
                "tone": "economic",
                "bias_notes": "Prioritises commercial impact and market confidence.",
            },
            MediaAlignment.NEUTRAL: {
                "headline": "Protest Ends After Police Intervention at City Square",
                "article": (
                    "NEXA News reports that a City Square protest ended after police "
                    "intervention. Authorities, union representatives and witnesses "
                    "offer different accounts of the events."
                ),
                "broadcast": (
                    "NEXA News: the City Square protest has ended, with conflicting "
                    "accounts emerging from those involved."
                ),
                "tone": "balanced",
                "bias_notes": "Presents a broad overview without adopting one faction's account.",
            },
        }[alignment]

        return MediaReport(
            content_type=MediaContentType.ARTICLE,
            organization_id=organization.id,
            organization_name=organization.name,
            alignment=alignment,
            event_id=event_id,
            event_type=event_type,
            headline=content["headline"],
            article=content["article"],
            broadcast=content["broadcast"],
            tone=content["tone"],
            bias_notes=content["bias_notes"],
            simulation_day=simulation_day,
        )

    def _generate_general_report(
        self,
        organization: MediaOrganization,
        event_id: str | None,
        event_type: str,
        description: str,
        simulation_day: int,
    ) -> MediaReport:
        alignment_prefix = {
            MediaAlignment.GOVERNMENT: "Officials Respond to",
            MediaAlignment.INDEPENDENT: "Investigation Continues Into",
            MediaAlignment.UNION: "Workers React to",
            MediaAlignment.CORPORATE: "Business Community Assesses",
            MediaAlignment.NEUTRAL: "NEXA City Responds to",
        }[organization.alignment]

        headline = f"{alignment_prefix} {event_type.replace('_', ' ').title()}"

        return MediaReport(
            content_type=MediaContentType.ARTICLE,
            organization_id=organization.id,
            organization_name=organization.name,
            alignment=organization.alignment,
            event_id=event_id,
            event_type=event_type,
            headline=headline,
            article=(
                f"{organization.name} reports: {description} "
                f"Coverage reflects its editorial focus: "
                f"{organization.editorial_position}"
            ),
            broadcast=f"{organization.name} broadcast: {headline}.",
            tone=organization.alignment.value,
            bias_notes=organization.editorial_position,
            simulation_day=simulation_day,
        )
