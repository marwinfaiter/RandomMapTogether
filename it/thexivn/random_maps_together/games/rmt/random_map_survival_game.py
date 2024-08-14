import asyncio

from it.thexivn.random_maps_together.configuration.rmt.rms_configuration import \
    RandomMapSurvivalConfiguration
from it.thexivn.random_maps_together.games.rmt import RMTGame
from it.thexivn.random_maps_together.map_generator import MapGenerator
from it.thexivn.random_maps_together.models.enums.game_modes import GameModes
from it.thexivn.random_maps_together.views.rmt.random_map_survival.ingame import \
    RandomMapSurvivalIngameView
from it.thexivn.random_maps_together.views.rmt.random_map_survival.settings import \
    RandomMapSurvivalSettingsView


class RandomMapSurvivalGame(RMTGame):
    game_mode = GameModes.RANDOM_MAP_SURVIVAL

    def __init__(self, app, *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        self.config = RandomMapSurvivalConfiguration(app, MapGenerator(app))
        self.config.update_player_configs()
        self.views.settings_view = RandomMapSurvivalSettingsView(app, self.config)
        self.views.ingame_view = RandomMapSurvivalIngameView(self)
        asyncio.gather(
            self.views.settings_view.display(),
            self.hide_timer(),
        )
