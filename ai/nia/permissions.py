from enum import Enum
from typing import Dict


class PermissionLevel(str, Enum):
    READ = "read"
    REQUEST = "request"
    APPROVED_ACTION = "approved_action"


TOOL_PERMISSIONS: Dict[str, PermissionLevel] = {
    "get_world_state": PermissionLevel.READ,
    "get_location": PermissionLevel.READ,
    "get_character": PermissionLevel.READ,
    "get_faction": PermissionLevel.READ,
    "get_recent_events": PermissionLevel.READ,
    "get_player_profile": PermissionLevel.READ,
    "search_memory": PermissionLevel.READ,
    "inspect_evidence": PermissionLevel.READ,
    "create_request": PermissionLevel.REQUEST,
    "trigger_event": PermissionLevel.APPROVED_ACTION,
    "send_message": PermissionLevel.APPROVED_ACTION,
    "change_relationship": PermissionLevel.APPROVED_ACTION,
    "request_camera_focus": PermissionLevel.APPROVED_ACTION,
}


class PermissionError(Exception):
    pass


class PermissionManager:
    """
    NIA has no direct authority to execute world-changing tools.
    """

    def can_use(self, tool_name: str, permission_level: PermissionLevel) -> bool:
        required = TOOL_PERMISSIONS.get(tool_name)

        if required is None:
            return False

        return required == permission_level

    def require(
        self,
        tool_name: str,
        permission_level: PermissionLevel,
    ) -> None:
        if not self.can_use(tool_name, permission_level):
            required = TOOL_PERMISSIONS.get(tool_name, "unknown")
            raise PermissionError(
                f"Tool '{tool_name}' requires '{required}' permission. "
                f"Direct execution is not permitted at '{permission_level}'."
            )
