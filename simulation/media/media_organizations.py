from typing import Dict, List, Optional

from media_models import MediaAlignment, MediaOrganization


class MediaOrganizations:
    """
    Registry of fictional media organisations in NEXA.
    """

    def __init__(self) -> None:
        self.organizations: Dict[str, MediaOrganization] = {}
        self.seed_default_organizations()

    def add(self, organization: MediaOrganization) -> MediaOrganization:
        self.organizations[organization.id] = organization
        return organization

    def get(self, organization_id: str) -> Optional[MediaOrganization]:
        return self.organizations.get(organization_id)

    def get_all(self) -> List[MediaOrganization]:
        return list(self.organizations.values())

    def get_by_alignment(
        self,
        alignment: MediaAlignment,
    ) -> List[MediaOrganization]:
        return [
            organization
            for organization in self.organizations.values()
            if organization.alignment == alignment
        ]

    def seed_default_organizations(self) -> None:
        organizations = [
            MediaOrganization(
                id="nexa_news",
                name="NEXA News",
                alignment=MediaAlignment.NEUTRAL,
                credibility=72.0,
                influence=78.0,
                audience_description="Broad citywide audience",
                editorial_position=(
                    "Fast, accessible reporting focused on major city events."
                ),
            ),
            MediaOrganization(
                id="city_herald",
                name="City Herald",
                alignment=MediaAlignment.GOVERNMENT,
                credibility=61.0,
                influence=70.0,
                audience_description="Government-aligned civic audience",
                editorial_position=(
                    "Emphasises public order, civic stability and official statements."
                ),
            ),
            MediaOrganization(
                id="independent_network",
                name="Independent Network",
                alignment=MediaAlignment.INDEPENDENT,
                credibility=84.0,
                influence=74.0,
                audience_description="Investigative and politically independent audience",
                editorial_position=(
                    "Focuses on evidence, public accountability and affected citizens."
                ),
            ),
            MediaOrganization(
                id="workers_voice",
                name="Workers Voice",
                alignment=MediaAlignment.UNION,
                credibility=68.0,
                influence=62.0,
                audience_description="Workers, union supporters and labour activists",
                editorial_position=(
                    "Reports events through worker rights and social justice concerns."
                ),
            ),
            MediaOrganization(
                id="corporate_signal",
                name="Corporate Signal",
                alignment=MediaAlignment.CORPORATE,
                credibility=55.0,
                influence=66.0,
                audience_description="Business, investor and corporate audience",
                editorial_position=(
                    "Emphasises market stability, enterprise and economic confidence."
                ),
            ),
        ]

        for organization in organizations:
            self.add(organization)
