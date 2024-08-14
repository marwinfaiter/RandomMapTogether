from attrs import define, field
from it.thexivn.random_maps_together.models.game_views import GameViews
from it.thexivn.random_maps_together.views.chess.board import ChessBoardView
from it.thexivn.random_maps_together.views.chess.ingame import ChessIngameView
from it.thexivn.random_maps_together.views.chess.settings import \
    ChessSettingsView


@define
class ChessViews(GameViews):
    settings_view: ChessSettingsView = field(init=False)
    ingame_view: ChessIngameView = field(init=False)
    board_view: ChessBoardView = field(init=False)
