from typing import Optional

from attrs import define
from it.thexivn.random_maps_together.models.database.chess.chess_move import \
    ChessMove
from it.thexivn.random_maps_together.models.database.chess.chess_piece import \
    ChessPiece
from it.thexivn.random_maps_together.models.enums.team import Team


@define
class Piece:
    team: Team
    x: int
    y: int
    db: Optional[ChessPiece] = None
    max_steps: Optional[int] = None
    captured: bool = False
    last_move: Optional[ChessMove] = None

    def moves(self):
        raise NotImplementedError("No moves implemented for piece")
