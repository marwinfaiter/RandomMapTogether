import logging

from it.thexivn.random_maps_together.configuration.rmt.rms_configuration import \
    RandomMapSurvivalConfiguration
from it.thexivn.random_maps_together.views.rmt.settings import \
    RandomMapsTogetherSettingsView

logger = logging.getLogger(__name__)

class RandomMapSurvivalSettingsView(RandomMapsTogetherSettingsView):
    template_name = "random_maps_together/rmt/random_map_survival/settings.xml"

    def __init__(self, app, config: RandomMapSurvivalConfiguration):
        super().__init__(app, config)
        self.subscribe("ui_set_goal_bonus_seconds", self.config.set_goal_bonus_seconds)
        self.subscribe("ui_set_skip_penalty_seconds", self.config.set_skip_penalty_seconds)
