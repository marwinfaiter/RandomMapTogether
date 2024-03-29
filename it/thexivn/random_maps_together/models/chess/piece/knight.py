from typing import Tuple

from attrs import define

from . import Piece


@define
class Knight(Piece):
    max_steps: int = 1

    def moves(self):
        return [
            self.move_left_up_left,
            self.move_left_up_up,
            self.move_right_up_up,
            self.move_right_up_right,
            self.move_right_down_right,
            self.move_right_down_down,
            self.move_left_down_down,
            self.move_left_down_left,
        ]

    def move_left_up_left(self, x: int) -> Tuple[int, int]:
        return (self.x - x * 2, self.y + x)

    def move_left_up_up(self, x: int) -> Tuple[int, int]:
        return (self.x - x, self.y + x * 2)

    def move_right_up_up(self, x: int) -> Tuple[int, int]:
        return (self.x + x, self.y + x * 2)

    def move_right_up_right(self, x: int) -> Tuple[int, int]:
        return (self.x + x * 2, self.y + x)

    def move_right_down_right(self, x: int) -> Tuple[int, int]:
        return (self.x + x * 2, self.y - x)

    def move_right_down_down(self, x: int) -> Tuple[int, int]:
        return (self.x + x, self.y - x * 2)

    def move_left_down_down(self, x: int) -> Tuple[int, int]:
        return (self.x - x, self.y - x * 2)

    def move_left_down_left(self, x: int) -> Tuple[int, int]:
        return (self.x - x * 2, self.y - x)
