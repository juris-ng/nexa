from typing import List, Optional

from director_models import EventProposal, ProposalStatus


class DirectorScheduler:
    """
    Keeps the Director's selected proposals awaiting validation.
    """

    def __init__(self) -> None:
        self.scheduled_proposals: List[EventProposal] = []

    def schedule(
        self,
        ranked_proposals: List[EventProposal],
    ) -> Optional[EventProposal]:
        if not ranked_proposals:
            return None

        selected = ranked_proposals[0]
        selected.status = ProposalStatus.SCHEDULED
        self.scheduled_proposals.append(selected)

        return selected

    def get_scheduled(self) -> List[EventProposal]:
        return self.scheduled_proposals.copy()

    def mark_validated(
        self,
        proposal_id: str,
    ) -> Optional[EventProposal]:
        for proposal in self.scheduled_proposals:
            if proposal.id == proposal_id:
                proposal.status = ProposalStatus.VALIDATED
                return proposal

        return None

    def mark_rejected(
        self,
        proposal_id: str,
    ) -> Optional[EventProposal]:
        for proposal in self.scheduled_proposals:
            if proposal.id == proposal_id:
                proposal.status = ProposalStatus.REJECTED
                return proposal

        return None
