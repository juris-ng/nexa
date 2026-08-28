from typing import Any, Dict

from context_manager import ContextManager


class ConversationService:
    """
    Phase 7 local conversation layer.

    It uses NEXA context to produce truthful prototype responses.
    A later LLM adapter will use this same context and permissions model.
    """

    def __init__(self, context_manager: ContextManager) -> None:
        self.context_manager = context_manager

    def respond(
        self,
        user_message: str,
        player_id: str | None = None,
    ) -> Dict[str, Any]:
        context = self.context_manager.build_context(
            user_message=user_message,
            player_id=player_id,
        )

        message = user_message.lower()
        response = self._create_response(message, context)

        return {
            "speaker": "NIA",
            "response": response,
            "context_summary": self.context_manager.summarise_context(context),
            "world_context": context,
        }

    def _create_response(
        self,
        message: str,
        context: Dict[str, Any],
    ) -> str:
        world_state = context["world_state"]
        events = context["recent_events"]

        if "what is happening" in message or "world state" in message:
            return (
                f"We are on simulation day {world_state['simulation_day']} at "
                f"{world_state['simulation_time']}. The weather is "
                f"{world_state['weather']}. Mayor approval is "
                f"{world_state['mayor_approval']}%, unemployment is "
                f"{world_state['unemployment_rate']}%, and union anger is "
                f"{world_state['union_anger']}%."
            )

        if "warehouse" in message:
            location = context["relevant_locations"][0]
            latest_event = events[-1] if events else None

            if latest_event:
                return (
                    f"The Eastern Warehouse is a {location['access_level']} "
                    f"site in the {location['district']}. A public labour "
                    f"dispute was recorded there after a corporation announced "
                    f"workforce reductions. The situation may affect "
                    f"unemployment, union anger and public confidence."
                )

            return (
                "I have no authorised recent public event linked to the "
                "Eastern Warehouse."
            )

        if "mayor" in message:
            mayor = context["relevant_characters"][0]

            return (
                f"{mayor['name']} is currently at the City Square, where she "
                f"is conducting a {mayor['current_activity']}. Her public "
                f"reputation is {mayor['reputation']}."
            )

        if "union" in message:
            union = context["relevant_factions"][0]

            return (
                f"The {union['name']} currently has public support of "
                f"{union['public_support']} and political power of "
                f"{union['political_power']}. Its stated ideology is: "
                f"{union['ideology']}."
            )

        if "investigate" in message:
            return (
                "I can help analyse public information and prepare an "
                "investigation request. I cannot directly alter the world "
                "or bypass location access rules. A validated audience-command "
                "system will decide whether the request can proceed."
            )

        return (
            "I am monitoring the NEXA world. Ask me about the current state, "
            "the Eastern Warehouse, the mayor, the union, or a recent event. "
            "I will distinguish confirmed information from uncertainty."
        )
