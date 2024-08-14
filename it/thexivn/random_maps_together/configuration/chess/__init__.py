from typing import Dict

from attrs import define, field
from pyplanet.apps.core.maniaplanet.models import Player

from it.thexivn.random_maps_together.configuration import Configuration
from it.thexivn.random_maps_together.map_generator import MapGenerator
from it.thexivn.random_maps_together.models.chess.player_configuration import PlayerConfiguration
from it.thexivn.random_maps_together.views.chess.player_config_view import PlayerConfigView


@define
class ChessConfiguration(Configuration):
    map_generator: MapGenerator
    player_configs: Dict[str, PlayerConfiguration] = field(factory=dict)

    def update_player_configs(self):
        for player in self.app.instance.player_manager.online:
            if player.login not in self.player_configs:
                self.player_configs[player.login] = PlayerConfiguration(
                    player,
                    False,
                )

    async def display_player_settings(self, player: Player, *_args, **_kwargs):
        self.update_player_configs()
        await PlayerConfigView(self.app).display(player)
        await PlayerConfigView(self.app).display(player)
