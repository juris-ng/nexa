from typing import Dict, List, Optional

from player_models import PlayerProfile


class PlayerService:
    """
    Holds and manages local player profiles.
    PostgreSQL persistence will replace this in the API/database integration.
    """

    def __init__(self) -> None:
        self.players: Dict[str, PlayerProfile] = {}

    def create_player(self, name: str) -> PlayerProfile:
        player = PlayerProfile(name=name)
        self.players[player.id] = player
        return player

    def get_player(self, player_id: str) -> Optional[PlayerProfile]:
        return self.players.get(player_id)

    def get_all_players(self) -> List[PlayerProfile]:
        return list(self.players.values())

    def add_reputation(
        self,
        player_id: str,
        change: float,
    ) -> Optional[PlayerProfile]:
        player = self.get_player(player_id)

        if player is None:
            return None

        player.change_reputation(change)
        return player
