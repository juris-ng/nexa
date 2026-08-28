from typing import Any, Dict, List

from media_models import MediaContentType, MediaReport
from media_organizations import MediaOrganizations
from news_generator import NewsGenerator
from rumour_engine import RumourEngine
from social_reaction_engine import SocialReactionEngine


class MediaEngine:
    """
    NEXA News and Media Engine.

    Events -> competing reports, broadcasts, rumours and social reactions.
    """

    def __init__(self) -> None:
        self.organizations = MediaOrganizations()
        self.news_generator = NewsGenerator()
        self.rumour_engine = RumourEngine()
        self.social_reaction_engine = SocialReactionEngine()
        self.reports: List[MediaReport] = []

    def process_event(
        self,
        event: Dict[str, Any],
        simulation_day: int,
    ) -> List[MediaReport]:
        generated: List[MediaReport] = []

        for organization in self.organizations.get_all():
            report = self.news_generator.generate(
                organization=organization,
                event=event,
                simulation_day=simulation_day,
            )
            generated.append(report)

        generated.extend(
            self.rumour_engine.generate(
                event=event,
                simulation_day=simulation_day,
            )
        )

        generated.extend(
            self.social_reaction_engine.generate(
                event=event,
                simulation_day=simulation_day,
            )
        )

        self.reports.extend(generated)
        return generated

    def get_recent_reports(
        self,
        limit: int = 20,
    ) -> List[Dict[str, Any]]:
        return [
            report.to_dict()
            for report in self.reports[-limit:]
        ]

    def get_reports_for_event(
        self,
        event_id: str,
    ) -> List[Dict[str, Any]]:
        return [
            report.to_dict()
            for report in self.reports
            if report.event_id == event_id
        ]

    def get_nia_media_context(
        self,
        event_id: str | None = None,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Returns public media context suitable for NIA.
        NIA should distinguish confirmed reports from rumours.
        """
        reports = (
            self.get_reports_for_event(event_id)
            if event_id
            else self.get_recent_reports(limit=limit)
        )

        return [
            report
            for report in reports
            if report["visibility"] == "public"
        ][-limit:]
