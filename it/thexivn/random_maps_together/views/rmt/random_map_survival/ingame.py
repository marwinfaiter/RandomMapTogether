import logging

from ....models.enums.game_modes import GameModes
from ..ingame import RandomMapsTogetherIngameView

logger = logging.getLogger(__name__)


class RandomMapSurvivalIngameView(RandomMapsTogetherIngameView):
    title = GameModes.RANDOM_MAP_SURVIVAL.value

    async def get_context_data(self):
        logger.info("Context Data")
        data = await super().get_context_data()
        data["skip_visible"] = True
        return data
