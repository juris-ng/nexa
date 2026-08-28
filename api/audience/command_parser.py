from command_models import AudienceCommand, CommandIntent


class CommandParser:
    """
    Phase 11 deterministic natural-language command parser.

    Later, an LLM-assisted NLP parser may be added, but validation will
    still use this same structured command format and rule layer.
    """

    TARGETS = {
        "warehouse": ("LOCATION", "eastern_warehouse"),
        "eastern warehouse": ("LOCATION", "eastern_warehouse"),
        "mayor": ("CHARACTER", "mayor_elena"),
        "mayor elena": ("CHARACTER", "mayor_elena"),
        "journalist": ("CHARACTER", "journalist_malik"),
        "malik": ("CHARACTER", "journalist_malik"),
        "corporation": ("ORGANIZATION", "nexa_corporation"),
        "protest": ("EVENT", "labour_protest"),
        "union": ("FACTION", "union"),
    }

    def parse(
        self,
        player_id: str,
        raw_text: str,
    ) -> AudienceCommand:
        message = raw_text.strip().lower()

        intent = self._detect_intent(message)
        target_type, target_id = self._detect_target(message)

        return AudienceCommand(
            player_id=player_id,
            raw_text=raw_text,
            intent=intent,
            target_type=target_type,
            target_id=target_id,
            metadata={
                "parser": "deterministic_phase_11",
            },
        )

    @staticmethod
    def _detect_intent(message: str) -> CommandIntent:
        if any(word in message for word in ("investigate", "inspect", "search")):
            return CommandIntent.INVESTIGATE

        if any(word in message for word in ("talk", "speak", "ask the mayor")):
            return CommandIntent.TALK

        if any(word in message for word in ("follow", "track", "watch")):
            return CommandIntent.FOLLOW

        if any(word in message for word in ("expose", "reveal", "publish")):
            return CommandIntent.EXPOSE

        if "ask nia" in message or message.startswith("nia"):
            return CommandIntent.ASK_NIA

        if any(word in message for word in ("vote", "support", "oppose")):
            return CommandIntent.VOTE

        return CommandIntent.UNKNOWN

    def _detect_target(
        self,
        message: str,
    ) -> tuple[str | None, str | None]:
        for keyword, target in self.TARGETS.items():
            if keyword in message:
                return target

        return None, None
