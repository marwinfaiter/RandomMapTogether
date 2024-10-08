import logging

from it.thexivn.random_maps_together.configuration.rmt.rmc_configuration import \
    RandomMapChallengeConfiguration
from it.thexivn.random_maps_together.views.rmt.settings import \
    RandomMapsTogetherSettingsView

logger = logging.getLogger(__name__)

class RandomMapChallengeSettingsView(RandomMapsTogetherSettingsView):
    template_name = "random_maps_together/rmt/random_map_challenge/settings.xml"

    def __init__(self, app, config: RandomMapChallengeConfiguration):
        super().__init__(app, config)
        self.subscribe("ui_toggle_infinite_skips", self.config.toggle_infinite_skips)
