from attrs import define
from typing import Optional

from ...enums.team import Team
from ...database.chess.chess_piece import ChessPiece
from ...database.chess.chess_move import ChessMove

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
