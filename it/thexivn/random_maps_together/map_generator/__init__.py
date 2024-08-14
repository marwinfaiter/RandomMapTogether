import logging
from enum import Enum
from typing import TYPE_CHECKING, Set

from it.thexivn.random_maps_together.models.api_response.api_map_info import APIMapInfo

if TYPE_CHECKING:
    from it.thexivn.random_maps_together.App import RandomMapsTogetherApp

logger = logging.getLogger(__name__)

class MapGeneratorType(Enum):
    RANDOM = "RANDOM"
    TOTD = "TOTD"
    CUSTOM = "CUSTOM"

class MapGenerator:
    def __init__(self, app: "RandomMapsTogetherApp"):
        self.map_generator_type = MapGeneratorType.RANDOM
        self.app = app
        self.played_maps: Set[APIMapInfo] = set()

    async def get_map(self):
        return await self.get_random_map()

    async def get_random_map(self) -> APIMapInfo:
        return await self.app.tmx_client.search_random_map()
        return await self.app.tmx_client.search_random_map()
