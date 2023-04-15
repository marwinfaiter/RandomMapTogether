from dataclasses import dataclass
from typing import Dict
from pyplanet.apps import AppConfig
from pyplanet.apps.core.maniaplanet.models import Player

from ..models.enums.medals import Medals
from ..map_generator import MapGenerator, MapGeneratorType
from ..map_generator.custom import Custom
from ..map_generator.totd import TOTD
from ..models.player_configuration import PlayerConfiguration
from ..games import check_player_allowed_to_change_game_settings
from ..views.player_config_view import PlayerConfigView
from ..views.player_prompt_view import PlayerPromptView

@dataclass
class Configuration:
    app: AppConfig
    goal_medal = Medals.AUTHOR
    skip_medal = Medals.GOLD
    enabled = True
    min_level_to_start = 1
    map_generator = None
    player_configs: Dict[str, PlayerConfiguration] = None

    def __post_init__(self):
        self.map_generator = MapGenerator(self.app)
        self.update_player_configs()

    def set_min_level_to_start(self, old_value: str, value: str):
        level = int(value)
        if level < 0:
            level = 0
        elif level > 3:
            level = 3

        self.min_level_to_start = level

    async def update_time_left(self, rmt_game, free_skip=False, goal_medal=False, skip_medal=False):
        pass

    def update_player_configs(self):
        if not self.player_configs:
            self.player_configs = {
                player.login: PlayerConfiguration(player)
                for player in self.app.instance.player_manager.online
            }
        else:
            for player in self.app.instance.player_manager.online:
                if not player.login in self.player_configs:
                    self.player_configs[player.login] = PlayerConfiguration(player)

    @check_player_allowed_to_change_game_settings
    async def set_goal_bonus_seconds(self, player: Player, caller, values, **kwargs):
        buttons = [
            {"name": "1m", "value": 60},
            {"name": "3m", "value": 180},
            {"name": "5m", "value": 300}
        ]
        time_seconds = await PlayerPromptView.prompt_for_input(player, "Goal bonus in seconds", buttons, default=self.goal_bonus_seconds)
        self.goal_bonus_seconds = int(time_seconds)
        await self.app.game.views.settings_view.display()

    @check_player_allowed_to_change_game_settings
    async def set_skip_penalty_seconds(self, player: Player, caller, values, **kwargs):
        buttons = [
            {"name": "30s", "value": 30},
            {"name": "1m", "value": 60},
            {"name": "2m", "value": 120}
        ]
        time_seconds = await PlayerPromptView.prompt_for_input(player, "Skip penalty in seconds", buttons, default=self.skip_penalty_seconds)
        self.skip_penalty_seconds = int(time_seconds)
        await self.app.game.views.settings_view.display()


    @check_player_allowed_to_change_game_settings
    async def set_goal_medal(self, player: Player, caller, values, **kwargs):
        self.goal_medal = Medals[caller.split("it_thexivn_RandomMapsTogether_settings__ui_set_goal_medal_")[1].upper()]
        await self.app.game.views.settings_view.display()

    @check_player_allowed_to_change_game_settings
    async def set_skip_medal(self, player: Player, caller, values, **kwargs):
        self.skip_medal = Medals[caller.split("it_thexivn_RandomMapsTogether_settings__ui_set_skip_medal_")[1].upper()]
        await self.app.game.views.settings_view.display()

    @check_player_allowed_to_change_game_settings
    async def toggle_infinite_skips(self, player: Player, *args, **kwargs):
        self.infinite_free_skips ^= True
        await self.app.game.views.settings_view.display()

    @check_player_allowed_to_change_game_settings
    async def toggle_allow_pausing(self, player: Player, *args, **kwargs):
        self.allow_pausing ^= True
        await self.app.game.views.settings_view.display()

    @check_player_allowed_to_change_game_settings
    async def set_map_generator(self, player, caller, values, **kwargs):
        map_generator_string = caller.split("it_thexivn_RandomMapsTogether_settings__ui_set_map_generator_")[1]
        if map_generator_string == "random" and self.map_generator.map_generator_type != MapGeneratorType.RANDOM:
            self.map_generator = MapGenerator(self.app)
            await self.app.map_handler.pre_load_next_map()
        elif map_generator_string == "totd" and self.map_generator.map_generator_type != MapGeneratorType.TOTD:
            self.map_generator = TOTD(self.app)
            await self.app.map_handler.pre_load_next_map()
        elif map_generator_string == "map_pack":
            if self.map_generator.map_generator_type != MapGeneratorType.CUSTOM:
                self.map_generator = Custom(self.app)
            await self.map_generator.maps_ui.display(player)

        await self.app.game.views.settings_view.display()

    @check_player_allowed_to_change_game_settings
    async def toggle_player_settings(self, player, caller, values, **kwargs):
        await PlayerConfigView(self.app).display(player)

    @check_player_allowed_to_change_game_settings
    async def toggle_enabled_players(self, player, caller, values, **kwargs):
        self.enabled ^= True
        await self.app.game.views.settings_view.display()
