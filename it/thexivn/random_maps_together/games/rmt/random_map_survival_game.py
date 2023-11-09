import asyncio

from ...configuration.rmt.rms_configuration import RandomMapSurvivalConfiguration
from ...map_generator import MapGenerator
from ...models.enums.game_modes import GameModes
from ...views.rmt.random_map_survival.ingame import RandomMapSurvivalIngameView
from ...views.rmt.random_map_survival.settings import RandomMapSurvivalSettingsView
from . import RMTGame


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
            self.hide_timer()
        )
