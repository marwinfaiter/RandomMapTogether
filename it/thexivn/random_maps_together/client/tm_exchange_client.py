from typing import List

import aiohttp

from it.thexivn.random_maps_together.models.api_response.api_map_info import APIMapInfo
from it.thexivn.random_maps_together.models.api_response.api_map_pack_info import (
    APIMapPackInfo,
)
from it.thexivn.random_maps_together.models.map_tag import MapTag


class TMExchangeClient:
    def __init__(self):
        self.base_url = "https://trackmania.exchange/"
        self.session = aiohttp.ClientSession(conn_timeout=10)
        self.map_tags: List[MapTag] = []

    async def get_json(self, url, params=None):
        async with self.session.get(f"{self.base_url}{url}", params=params) as response:
            response.raise_for_status()
            return await response.json()

    async def get_content(self, url, params=None):
        async with self.session.get(f"{self.base_url}{url}", params=params) as response:
            response.raise_for_status()
            return await response.read()

    async def search_map(self, params=None) -> List[APIMapInfo]:
        response = await self.get_json("api/maps",
            {
                "fields": "MapId,MapUid,UpdatedAt,Uploader.Name,Name,Tags",
                **(params if params else {}),
            }
        )
        return [
            APIMapInfo.from_json(map_json)
            for map_json in response.get("Results", [])
        ]

    async def search_random_map(self) -> APIMapInfo:
        maps = await self.search_map({
            "count": 1,
            "random": 1,
            "lengthmax": 9,
            "etag": "23,46,40,41,42,37",
        })
        return maps.pop()

    async def search_mappack(self, params=None):
        response = await self.get_json("api/mappacks",
            {
                "fields": "MappackId,Name,MapCount",
                **(params if params else {}),
            }
        )
        return [
            APIMapPackInfo.from_json(map_pack_json)
            for map_pack_json in response.get("Results", [])
        ]

    async def search_random_mappack_totd(self):
        map_packs = await self.search_mappack({
            "count": 1,
            "random": 1,
            "manageruserid": 21,
            "name": "TOTD - Track of the Day",
        })
        return map_packs.pop()

    async def get_map_info_by_id(self, map_id):
        maps = await self.search_map({"id": map_id})
        return maps.pop()

    async def get_mappack_info_by_id(self, map_pack_id):
        return await self.get_json(f"api/mappack/get_info/{map_pack_id}")

    async def get_mappack_tracks(self, map_pack_id):
        return await self.search_map({"mappackid": map_pack_id})

    async def get_tags(self) -> List[MapTag]:
        if self.map_tags:
            return self.map_tags

        self.map_tags = [
            MapTag.from_json(tag_json)
            for tag_json in await self.get_json("api/tags/gettags")
        ]

        return self.map_tags

    async def get_map_content(self, map_id):
        return await self.get_content(f"maps/download/{map_id}")
