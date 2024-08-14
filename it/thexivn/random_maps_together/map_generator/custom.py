import logging
import random
from typing import Set

from it.thexivn.random_maps_together.map_generator import (MapGenerator,
                                                           MapGeneratorType)
from it.thexivn.random_maps_together.models.api_response.api_map_info import \
    APIMapInfo
from it.thexivn.random_maps_together.views.custom_maps_view import \
    CustomMapsView

logger = logging.getLogger(__name__)


class Custom(MapGenerator):
    def __init__(self, app):
        super().__init__(app)
        self.map_generator_type = MapGeneratorType.CUSTOM
        self.maps: Set[APIMapInfo] = set()
        self.maps_ui = CustomMapsView(app)

    async def add_map(self, map_id):
        self.maps.add(await self.app.tmx_client.get_map_info_by_id(map_id))

    async def add_map_pack(self, map_pack_id):
        self.maps.update(await self.app.tmx_client.get_mappack_tracks(map_pack_id))

    async def remove_map(self, map_id):
        self.maps.remove(next(played_map for played_map in self.maps if played_map.TrackID == map_id))

    async def get_map(self) -> APIMapInfo:
        non_played_maps = [played_map for played_map in self.maps if played_map not in self.played_maps]
        if non_played_maps:
            return random.choice(non_played_maps)  # noqa: S311

        return await self.get_random_map()

    async def map_pack_id_validator(self, map_pack_id):
        try:
            await self.app.tmx_client.get_mappack_info_by_id(map_pack_id)
        except Exception as exc:
            raise ValueError(f"Mappack does not exist: {map_pack_id}") from exc

    async def map_id_validator(self, map_id):
        try:
            await self.app.tmx_client.get_map_info_by_id(map_id)
        except Exception as exc:
            raise ValueError(f"Map ID does not exist: {map_id}") from exc
