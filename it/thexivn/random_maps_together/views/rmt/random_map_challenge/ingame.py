import logging

from it.thexivn.random_maps_together.models.enums.game_modes import GameModes
from it.thexivn.random_maps_together.views.rmt.ingame import \
    RandomMapsTogetherIngameView

logger = logging.getLogger(__name__)


class RandomMapChallengeIngameView(RandomMapsTogetherIngameView):
    title = GameModes.RANDOM_MAP_CHALLENGE.value

    async def get_context_data(self):
        logger.info("Context Data")
        data = await super().get_context_data()
        data["skip_visible"] = self.game.config.infinite_free_skips
        return data
