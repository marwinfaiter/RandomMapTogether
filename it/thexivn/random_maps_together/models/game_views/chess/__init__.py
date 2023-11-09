from attrs import define, field

from ....views.chess.board import ChessBoardView
from ....views.chess.ingame import ChessIngameView
from ....views.chess.settings import ChessSettingsView
from .. import GameViews


@define
class ChessViews(GameViews):
    settings_view: ChessSettingsView = field(init=False)
    ingame_view: ChessIngameView = field(init=False)
    board_view: ChessBoardView = field(init=False)
