from typing import Any, Dict

from nia_persona import NIA_NAME, get_persona_summary
from request_queue import RequestQueue
from world_tools import WorldTools
from context_manager import ContextManager
from conversation_service import ConversationService


class NIAAgent:
    """
    Main NIA coordinator.

    Flow:
    User -> NIA Agent -> Context Manager -> Memory/World Tools
         -> Conversation Service -> Response / Controlled Request
    """

    def __init__(self) -> None:
        self.request_queue = RequestQueue()
        self.world_tools = WorldTools(self.request_queue)
        self.context_manager = ContextManager(self.world_tools)
        self.conversation_service = ConversationService(self.context_manager)

    def introduce(self) -> str:
        return f"{NIA_NAME}: {get_persona_summary()}"

    def chat(
        self,
        user_message: str,
        player_id: str | None = None,
    ) -> Dict[str, Any]:
        return self.conversation_service.respond(
            user_message=user_message,
            player_id=player_id,
        )

    def create_action_request(
        self,
        request_type: str,
        payload: Dict[str, Any],
        reason: str,
    ) -> Dict[str, Any]:
        return self.world_tools.create_request(
            request_type=request_type,
            payload=payload,
            reason=reason,
        )

    def get_pending_requests(self) -> list[Dict[str, Any]]:
        return [
            request.to_dict()
            for request in self.request_queue.get_pending_requests()
        ]
