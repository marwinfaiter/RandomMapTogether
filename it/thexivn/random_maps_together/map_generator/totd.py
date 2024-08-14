import logging
import random
from typing import List

from it.thexivn.random_maps_together.map_generator import MapGenerator, MapGeneratorType
from it.thexivn.random_maps_together.models.api_response.api_map_info import APIMapInfo

logger = logging.getLogger(__name__)


class TOTD(MapGenerator):
    def __init__(self, app):
        super().__init__(app)
        self.map_generator_type = MapGeneratorType.TOTD

    async def get_map(self) -> APIMapInfo:
        map_pack = await self.app.tmx_client.search_random_mappack_totd()
        map_pack_tracks: List[APIMapInfo] = await self.app.tmx_client.get_mappack_tracks(map_pack.id)
        return random.choice([played_map for played_map in map_pack_tracks if played_map not in self.played_maps])  # noqa: S311
        map_pack_tracks: List[APIMapInfo] = await self.app.tmx_client.get_mappack_tracks(map_pack.id)
        return random.choice([played_map for played_map in map_pack_tracks if played_map not in self.played_maps])  # noqa: S311
