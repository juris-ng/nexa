from typing import Dict, List, Optional

from mystery_models import Evidence, EvidenceVisibility


class EvidenceEngine:
    """
    Stores and controls discovery of evidence.
    """

    def __init__(self) -> None:
        self.evidence: Dict[str, Evidence] = {}

    def add_evidence(self, evidence: Evidence) -> Evidence:
        self.evidence[evidence.id] = evidence
        return evidence

    def get_evidence(self, evidence_id: str) -> Optional[Evidence]:
        return self.evidence.get(evidence_id)

    def reveal_evidence(
        self,
        evidence_id: str,
        simulation_day: int,
        visibility: EvidenceVisibility = EvidenceVisibility.DISCOVERED,
    ) -> Optional[Evidence]:
        evidence = self.get_evidence(evidence_id)

        if evidence is None:
            return None

        evidence.visibility = visibility
        evidence.discovered_at_day = simulation_day
        return evidence

    def get_visible_evidence(
        self,
        visibility_levels: List[EvidenceVisibility] | None = None,
    ) -> List[Evidence]:
        levels = visibility_levels or [
            EvidenceVisibility.DISCOVERED,
            EvidenceVisibility.PUBLIC,
        ]

        return [
            evidence
            for evidence in self.evidence.values()
            if evidence.visibility in levels
        ]

    def get_evidence_for_mystery(
        self,
        evidence_ids: List[str],
    ) -> List[Evidence]:
        return [
            self.evidence[evidence_id]
            for evidence_id in evidence_ids
            if evidence_id in self.evidence
        ]
