import logging
from typing import Any, ClassVar, Dict

from pyplanet.views.generics.widget import WidgetView

logger = logging.getLogger(__name__)


class SettingsView(WidgetView):
    widget_x = -100
    widget_y = 73.5
    z_index = 5
    size_x = 66
    size_y = 9
    data: ClassVar[Dict[str, Any]] = {}

    def __init__(self, app, config):
        super().__init__()
        logger.info("Loading VIEW")
        self.id = "it_thexivn_RandomMapsTogether_settings"
        self.app = app
        self.manager = app.context.ui
        self.config = config
        self.subscribe("ui_start", self.app.start_game)
        self.subscribe("ui_set_map_generator_random", self.config.set_map_generator)
        self.subscribe("ui_set_map_generator_totd", self.config.set_map_generator)
        self.subscribe("ui_set_map_generator_map_pack", self.config.set_map_generator)
        self.subscribe("ui_display_player_settings", self.config.display_player_settings)
        self.subscribe("ui_display_leaderboard", self.config.display_leaderboard)
