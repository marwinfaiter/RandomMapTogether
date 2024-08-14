from typing import Tuple

from attrs import define
from it.thexivn.random_maps_together.models.chess.piece import Piece
from it.thexivn.random_maps_together.models.enums.team import Team


@define
class Pawn(Piece):
    max_steps: int = 1

    def moves(self):
        return [
            self.move_left_forward,
            self.move_forward,
            self.move_forward_forward,
            self.move_right_forward,
        ]

    def move_left_forward(self, x: int) -> Tuple[int, int]:
        if self.team == Team.BLACK:
            return (self.x - x, self.y - x)

        if self.team == Team.WHITE:
            return (self.x - x, self.y + x)

        raise RuntimeError(f"Invalid team: {self.team}")

    def move_forward(self, x: int) -> Tuple[int, int]:
        if self.team == Team.BLACK:
            return (self.x, self.y - x)

        if self.team == Team.WHITE:
            return (self.x, self.y + x)

        raise RuntimeError(f"Invalid team: {self.team}")

    def move_forward_forward(self, x: int) -> Tuple[int, int]:
        if self.team == Team.BLACK:
            return (self.x, self.y - x * 2)

        if self.team == Team.WHITE:
            return (self.x, self.y + x * 2)

        raise RuntimeError(f"Invalid team: {self.team}")

    def move_right_forward(self, x: int) -> Tuple[int, int]:
        if self.team == Team.BLACK:
            return (self.x + x, self.y - x)

        if self.team == Team.WHITE:
            return (self.x + x, self.y + x)

        raise RuntimeError(f"Invalid team: {self.team}")
