import asyncio
import logging
import time as py_time

from pyplanet.apps.core.maniaplanet.models import Player
from pyplanet.contrib.chat import ChatManager
from pyplanet.contrib.mode import ModeManager

from it.thexivn.random_maps_together import MapHandler
from it.thexivn.random_maps_together.Data.Configurations import Configurations
from it.thexivn.random_maps_together.Data.GameScore import GameScore
from it.thexivn.random_maps_together.Data.GameState import GameState

from it.thexivn.random_maps_together.views import RandomMapsTogetherView

S_TIME_LIMIT = 'S_TimeLimit'
_lock = asyncio.Lock()

logger = logging.getLogger(__name__)


class RMTGame:
    def __init__(self, map_handler: MapHandler, chat: ChatManager, mode_manager: ModeManager,
                 score_ui: RandomMapsTogetherView, config: Configurations):
        self._rmt_starter_player: Player = None
        self._score = GameScore()
        self._map_handler = map_handler
        self._chat = chat
        self._mode_manager = mode_manager
        self._mode_settings = None
        self._map_start_time = py_time.time()
        self._config = config
        self._time_left = config.game_time_seconds
        self._score_ui = score_ui
        self._game_state = GameState()
        self._score_ui.set_score(self._score)

        logger.info("RMT Game initialized")

    async def on_init(self):
        await self._map_handler.load_hub()
        logger.info("RMT Game loaded")
        self._mode_settings = await self._mode_manager.get_settings()
        await self.hide_timer()
        await self._score_ui.display()
        self._score_ui.subscribe("ui_gold_skips", self.command_skip_gold)
        self._score_ui.subscribe("ui_start_rmt", self.command_start_rmt)
        self._score_ui.subscribe("ui_stop_rmt", self.command_stop_rmt)

    async def command_start_rmt(self, player: Player, *args, **kwargs):
        if self._game_state.is_hub_stage():
            self._game_state.set_start_new_state()
            await self._chat(f'{player.nickname} started new RMT, loading next map ...')
            self._rmt_starter_player = player
            self._time_left = self._config.game_time_seconds
            self._mode_settings[S_TIME_LIMIT] = self._time_left
            if await self.load_with_retry():
                logger.info("RMT started")
                self._game_state.game_is_in_progress = True
            else:
                self._game_state.set_hub_state()
                self._mode_settings[S_TIME_LIMIT] = 0
                await self._chat("RMT failed to start")
            await self._mode_manager.update_settings(self._mode_settings)
        else:
            await self._chat("RMT already started", player)

    async def load_with_retry(self, max_retry=3) -> bool:
        retry = 0
        load_succeeded = False
        self._game_state.map_is_loading = True
        while not load_succeeded and retry < max_retry:
            retry += 1
            try:
                await self._map_handler.load_next_map()
                load_succeeded = True
            except Exception as e:
                logger.error("failed to load map...", exc_info=e)
                await self._map_handler.remove_loaded_map()

        self._game_state.map_is_loading = False
        return retry < max_retry

    async def command_stop_rmt(self, player: Player, *args, **kwargs):
        if self._game_state.is_game_stage():
            if player == self._rmt_starter_player:
                await self._chat(f'{player.nickname} stopped new RMT')
                await self.back_to_hub()
            else:
                await self._chat("you can't stop the RMT", player)
        else:
            await self._chat("RMT is not started yet")

    async def back_to_hub(self):
        if self._game_state.is_game_stage():
            logger.info("Back to HUB ...")
            await self.hide_timer()
            self._game_state.set_hub_state()
            self._score.rest()
            await self._score_ui.display()
            await self._map_handler.remove_loaded_map()
            await self._map_handler.load_hub()
            self._rmt_starter_player = None
            logger.info("Back to HUB completed")

    async def map_begin_event(self, map, *args, **kwargs):
        logger.info("MAP Begin")
        self._map_handler.active_map = map
        self._score_ui.ui_controls_visible = True
        if self._game_state.is_game_stage():
            self._game_state.set_new_map_in_game_state()
            self._map_start_time = py_time.time()
        else:
            await self.hide_timer()
            self._game_state.current_map_completed = True

        await self._score_ui.display()

    async def map_end_event(self, time, count, *args, **kwargs):
        logger.info("MAP end")
        if self._game_state.is_game_stage():
            self._game_state.gold_skip_available = False
            self._score_ui.ui_controls_visible = False
            if not self._game_state.current_map_completed:
                logger.info("RMT finished successfully")
                await self._chat(
                    f'Challenge completed AT:{self._score.total_at} Gold:{self._score.total_gold}. peepoClap')
                await self.back_to_hub()
            else:
                self._mode_settings[S_TIME_LIMIT] = self._time_left
                logger.info("Continue with %d time left", self._time_left)
                await self._mode_manager.update_settings(self._mode_settings)

        await self._score_ui.display()

    async def on_map_finsh(self, player: Player, race_time: int, lap_time: int, cps, lap_cps, race_cps, flow,
                           is_end_race: bool, is_end_lap, raw, *args, **kwargs):
        logger.info(f'[on_map_finsh] {player.nickname} has finished the map with time: {race_time}ms')
        if self._game_state.is_game_stage():
            await _lock.acquire()  # lock to avoid multiple AT before next map is loaded
            if self._game_state.current_map_completed:
                logger.info(f'[on_map_finish] Map was already completed')
                _lock.release()
                return

            if is_end_race:
                logger.info(f'[on_map_finish] Final time check for AT')
                if race_time <= self._map_handler.at_time:
                    logger.info(f'[on_map_finish] AT Time acquired')
                    self._update_time_left()
                    self._game_state.set_map_completed_state()
                    await self.hide_timer()
                    _lock.release()  # with loading True don't need to lock
                    await self._chat(f'AT TIME, congratulations to {player.nickname}')
                    if await self.load_with_retry():
                        self._score.inc_at()
                    else:
                        await self.back_to_hub()
                elif race_time <= self._map_handler.gold_time:
                    logger.info(f'[on_map_finish] GOLD Time acquired')
                    self._game_state.gold_skip_available = True
                    _lock.release()
                    await self._chat(f'GOLD TIME now {player.nickname} can /skip_gold to load next map')
                else:
                    logger.info(f'[on_map_finish] Normal Time acquired')
                    _lock.release()
            else:
                _lock.release()

    async def command_skip_gold(self, player: Player, *args, **kwargs):
        if self._game_state.skip_command_allowed():
            if self._game_state.gold_skip_available:
                if self._rmt_starter_player == player:
                    self._update_time_left()
                    self._game_state.set_map_completed_state()
                    await self._chat(f'{player.nickname} decided to GOLD skip')
                    await self.hide_timer()
                    if await self.load_with_retry():
                        self._score.inc_gold()
                    else:
                        await self.back_to_hub()
            else:
                await self._chat("Gold skip is not available", player)
        else:
            await self._chat("You are not allowed to skip", player)

    async def hide_timer(self):
        self._mode_settings[S_TIME_LIMIT] = 0
        await self._mode_manager.update_settings(self._mode_settings)

    def _update_time_left(self):
        self._time_left -= int(py_time.time() - self._map_start_time)
