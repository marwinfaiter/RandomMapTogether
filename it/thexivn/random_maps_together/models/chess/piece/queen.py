from attrs import define
from typing import Tuple

from . import Piece


@define
class Queen(Piece):
    # pylint: disable=duplicate-code
    def moves(self):
        return [
            self.move_left,
            self.move_left_up,
            self.move_up,
            self.move_right_up,
            self.move_right,
            self.move_right_down,
            self.move_down,
            self.move_left_down,
        ]

    def move_left(self, x: int) -> Tuple[int, int]:
        return (self.x - x, self.y)

    def move_left_up(self, x: int) -> Tuple[int, int]:
        return (self.x - x, self.y + x)

    def move_up(self, x: int) -> Tuple[int, int]:
        return (self.x, self.y + x)

    def move_right_up(self, x: int) -> Tuple[int, int]:
        return (self.x + x, self.y + x)

    def move_right(self, x: int) -> Tuple[int, int]:
        return (self.x + x, self.y)

    def move_right_down(self, x: int) -> Tuple[int, int]:
        return (self.x + x, self.y - x)

    def move_down(self, x: int) -> Tuple[int, int]:
        return (self.x, self.y - x)

    def move_left_down(self, x: int) -> Tuple[int, int]:
        return (self.x - x, self.y - x)
