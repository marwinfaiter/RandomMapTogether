import asyncio

from ...configuration.rmt.rmc_configuration import RandomMapChallengeConfiguration
from ...map_generator import MapGenerator
from ...models.enums.game_modes import GameModes
from ...views.rmt.random_map_challenge.ingame import RandomMapChallengeIngameView
from ...views.rmt.random_map_challenge.settings import RandomMapChallengeSettingsView
from . import RMTGame


class RandomMapChallengeGame(RMTGame):
    game_mode = GameModes.RANDOM_MAP_CHALLENGE

    def __init__(self, app, *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        self.config = RandomMapChallengeConfiguration(app, MapGenerator(app))
        self.views.settings_view = RandomMapChallengeSettingsView(app, self.config)
        self.views.ingame_view = RandomMapChallengeIngameView(self)
        asyncio.gather(
            self.views.settings_view.display(),
            self.hide_timer()
        )
