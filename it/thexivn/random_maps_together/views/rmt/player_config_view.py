import logging
from typing import List, Dict
from peewee import DoesNotExist
from pyplanet.views.generics.list import ManualListView
from pyplanet.apps.config import AppConfig
from pyplanet.apps.core.maniaplanet.models import Player

from ...models.enums.medals import Medals
from ...models.database.rmt.rmt_player_score import RMTPlayerScore
from ..player_prompt_view import PlayerPromptView
from ...configuration import check_player_allowed_to_change_game_settings
# pylint: disable=duplicate-code
logger = logging.getLogger(__name__)

class PlayerConfigView(ManualListView): # pylint: disable=duplicate-code
    app: AppConfig = None

    title = 'Player Configs' # pylint: disable=duplicate-code
    template_name = "random_maps_together/list.xml"
    icon_style = 'Icons128x128_1'
    icon_substyle = 'Browse'

    data: List[Dict] = []

    def __init__(self, app):
        super().__init__(self)
        self.app = app
        self.manager = app.context.ui

    async def get_fields(self):
        return [
            {
                'name': 'Player',
                'index': 'player_nickname',
                'sorting': True,
                'searching': True,
                'width': 70,
                'type': 'label',
            },
            {
                'name': 'Player Login',
                'index': 'player_login',
                'sorting': True,
                'searching': True,
                'width': 70,
                'type': 'label',
            },
            {
                'name': 'Goal Medal',
                'index': 'goal_medal',
                'sorting': True,
                'searching': False,
                'width': 30,
                'action': self.prompt_for_goal_medal
            },
            {
                'name': 'Skip Medal',
                'index': 'skip_medal',
                'sorting': True,
                'searching': False,
                'width': 30,
                'action': self.prompt_for_skip_medal
            },
        ]

    async def get_actions(self):
        return [
            {
                    'name': 'Enabled',
                    'action': self.action_toggle_enabled_player,
                    'style': 'Icons64x64_1',
                    'substyle': 'Check',
                    'attrs_renderer': self._render_action_attr,
            },
        ]

    async def get_data(self):
        self.app.game.config.update_player_configs()
        return [
            {
                "player_nickname": player_config.player.nickname,
                "player_login": player_config.player.login,
                "goal_medal": player_config.goal_medal.name if player_config.goal_medal else None,
                "skip_medal": player_config.skip_medal.name if player_config.skip_medal else None,
            }
            for player_config in sorted(self.app.game.config.player_configs.values(), key=lambda x: x.player.nickname)
        ]

    def _render_action_attr(self, row, _action):
        return [
            {
                "key": "styleselected",
                "value": self.app.game.config.player_configs[row["player_login"]].enabled \
                    if self.app.game.config.player_configs[row["player_login"]].enabled is not None \
                    else self.app.game.config.enabled
            }
        ]

    @check_player_allowed_to_change_game_settings
    async def action_toggle_enabled_player(self, player, _values, row, **_kwargs):
        input_value = await PlayerPromptView.prompt_for_input(
            player, f"Enable or disable player, OK for global player enabled: {self.app.game.config.enabled}",
            [
                {"name": "Enable", "value": True},
                {"name": "Disable", "value": False},
            ],
            entry=False
        )
        self.app.game.config.player_configs[row["player_login"]].enabled = input_value
        await self.refresh(player=player)

    @check_player_allowed_to_change_game_settings
    async def prompt_for_goal_medal(self, player, _values, row, **_kwargs):
        buttons = [
            {"name": medal.name, "value": medal}
            for medal in [Medals.AUTHOR, Medals.GOLD, Medals.SILVER]
        ]

        medal = await PlayerPromptView.prompt_for_input(
            player, f"Goal Medal, OK for global Goal Medal: {self.app.game.config.goal_medal.name}",
            buttons=buttons, entry=False
        )
        self.app.game.config.player_configs[row["player_login"]].goal_medal = medal
        if self.app.game.game_is_in_progress:
            try:
                player_score = await RMTPlayerScore.get(
                    game_score=self.app.game.score.id,
                    player=(await Player.get_by_login(row["player_login"])).id,
                )
                player_score.goal_medal = medal.name if medal else None
                await player_score.save()
            except DoesNotExist:
                pass


        await self.refresh(player=player)

    @check_player_allowed_to_change_game_settings
    async def prompt_for_skip_medal(self, player, _values, row, **_kwargs):
        buttons = [
            {"name": medal.name, "value": medal}
            for medal in [Medals.GOLD, Medals.SILVER, Medals.BRONZE]
        ]

        medal = await PlayerPromptView.prompt_for_input(
            player, f"Skip Medal, OK for global Skip Medal: {self.app.game.config.skip_medal.name}",
            buttons=buttons, entry=False
        )
        self.app.game.config.player_configs[row["player_login"]].skip_medal = medal
        if self.app.game.game_is_in_progress:
            try:
                player_score = await RMTPlayerScore.get(
                    game_score=self.app.game.score.id,
                    player=(await Player.get_by_login(row["player_login"])).id,
                )
                player_score.skip_medal = medal.name if medal else None
                await player_score.save()
            except DoesNotExist:
                pass

        await self.refresh(player=player)
