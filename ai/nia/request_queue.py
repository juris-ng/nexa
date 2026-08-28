from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List
import uuid


@dataclass
class NIARequest:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    request_type: str = "general"
    requested_by: str = "NIA"
    payload: Dict[str, Any] = field(default_factory=dict)
    reason: str = ""
    status: str = "pending"
    created_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "request_type": self.request_type,
            "requested_by": self.requested_by,
            "payload": self.payload,
            "reason": self.reason,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
        }


class RequestQueue:
    """
    Stores proposed NIA actions until a later command and validation layer
    approves, rejects or executes them.
    """

    def __init__(self) -> None:
        self.requests: List[NIARequest] = []

    def create_request(
        self,
        request_type: str,
        payload: Dict[str, Any],
        reason: str,
    ) -> NIARequest:
        request = NIARequest(
            request_type=request_type,
            payload=payload,
            reason=reason,
        )
        self.requests.append(request)
        return request

    def get_pending_requests(self) -> List[NIARequest]:
        return [
            request
            for request in self.requests
            if request.status == "pending"
        ]

    def update_status(self, request_id: str, status: str) -> NIARequest | None:
        for request in self.requests:
            if request.id == request_id:
                request.status = status
                return request

        return None
