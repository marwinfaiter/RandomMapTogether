import json
from unittest import IsolatedAsyncioTestCase

from aiohttp import ClientSession
from it.thexivn.random_maps_together.client.tm_exchange_client import TMExchangeClient
from it.thexivn.random_maps_together.models.api_response.api_map_info import APIMapInfo
from it.thexivn.random_maps_together.models.api_response.api_map_pack_info import (
    APIMapPackInfo,
)
from mockito import KWARGS, expect, unstub, verifyNoUnwantedInteractions

from ..map_tags import TestMapTags  # noqa: TID252


class MockedResponse:
    def __init__(self, data, status):
        self.data = data
        self.status = status

    async def json(self):
        return self.data

    async def read(self):
        return json.dumps(self.data).encode("utf-8")

    def raise_for_status(self):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, *err):
        pass

class TestTMXClient(IsolatedAsyncioTestCase):
    def setUp(self):
        self.base_url = "https://trackmania.exchange"
        self.tmx_client = TMExchangeClient()
        self.test_map_tags = TestMapTags()

    def tearDown(self):
        verifyNoUnwantedInteractions()
        unstub()

    async def test_get_tags(self):
        expect(ClientSession, times=1).get(
            f"{self.base_url}/api/tags/gettags", **KWARGS,
        ).thenReturn(
            MockedResponse(self.test_map_tags.expected_map_tags(), 200),
        )
        assert await self.tmx_client.get_tags() == self.test_map_tags.expected_map_tags_as_objects()

    async def test_search_random_map(self):
        expect(ClientSession, times=1).get(
            f"{self.base_url}/api/maps", **KWARGS,
        ).thenReturn(
            MockedResponse(self._expected_map_search(), 200),
        )
        assert await self.tmx_client.search_random_map() == APIMapInfo.from_json(self._expected_map())

    async def test_search_mappack(self):
        expect(ClientSession, times=1).get(
            f"{self.base_url}/api/mappacks", **KWARGS,
        ).thenReturn(
            MockedResponse(self._expected_map_pack_search(), 200),
        )
        assert await self.tmx_client.search_mappack() == [APIMapPackInfo.from_json(self._expected_map_pack())]


    def _expected_map_search(self):
        return {
            "Result": [self._expected_map()],
        }

    def _expected_map(self):
        return {
            "MapId": 229788,
            "MapUid": "oNSbGPYPbNiAJ37gsjAkL5oqnRb",
            "UpdatedAt": "2025-03-06T15:55:17.491",
            "Uploader": {
                "Name": "koomah",
            },
            "Tags": [
                {
                    "TagId": 15,
                    "Name": "Dirt",
                    "Color": "5e2d09",
                },
                {
                    "TagId": 32,
                    "Name": "Transitional",
                    "Color": "",
                }
            ],
            "Name": "go",
        }

    def _expected_map_pack_search(self):
        return {
            "Results": [self._expected_map_pack()],
        }

    def _expected_map_pack(self):
        return {
            "MappackId": 1567,
            "MapCount": 29,
            "Name": "TOTD - Track of the Day - May 2022",
        }
