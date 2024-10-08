import logging

from it.thexivn.random_maps_together.models.database.chess.chess_score import \
    ChessScore
from pyplanet.views import TemplateView

logger = logging.getLogger(__name__)

class ChessBoardView(TemplateView):
    template_name = "random_maps_together/chess/board.xml"

    def __init__(self, game):
        super().__init__(self)
        logger.info("Loading VIEW")
        self.game = game
        self.manager = game.app.context.ui
        self.game_score: ChessScore
        self.id = "it_thexivn_RandomMapsTogether_scoreboard"
        self.subscribe("ui_hide_board", self.hide)
        for x in range(8):
            for y in range(8):
                self.subscribe(f"ui_display_piece_moves_{x}_{y}", self.game.display_piece_moves)
                self.subscribe(f"ui_move_piece_{x}_{y}", self.game.move_piece)

    async def get_context_data(self):
        data = await super().get_context_data()
        data["pieces"] = self.game.game_state.pieces_in_play
        data["moves"] = self.game.game_state.get_moves_for_piece(self.game.game_state.current_piece)
        data["current_king"] = self.game.game_state.current_king
        data["king_in_check"] = any(self.game.game_state.get_pieces_attacking_current_king())
        data["turn"] = self.game.game_state.turn
        if not data["moves"]:
            self.game.game_state.current_piece = None
        return data

    async def display(self, player=None, _button_id="", _values=None): # pylint: disable=arguments-renamed,arguments-differ
        if player:
            await super().display([player.login])
        else:
            await super().display()

    async def hide(self, player=None, _button_id="", _values=None): # pylint: disable=arguments-renamed,arguments-differ
        if player:
            await super().hide([player.login])
        else:
            await super().hide()
