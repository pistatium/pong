from typing import Tuple
from enum import Enum

import pyxel


BOARD_WIDTH = 192
BOARD_HEIGHT = 128
PADDING = 3
WIDTH = 192 + PADDING * 2
HEIGHT = 128 + PADDING + 12
BALL_SIZE = 4


class Color(Enum):
    BLACK = 0
    GRAY = 6
    GREEN = 11


class Ball:
    size: int
    x: int
    y: int
    vx: float
    vy: float

    def __init__(self, size: int, x: int, y: int, vx: float, vy: float):
        self.size = size
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def updated():
        self.x += self.vx
        self.y += self.vy
        self.vx *= self.friction
        self.vy *= self.friction


class Board:
    width: int
    height: int
    offset_x: int
    offset_y: int
    ball: Ball

    def __init__(self, width: int, height: int, offset_x: int, offset_y: int):
        self.width = width
        self.height = height
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.ball = Ball(BALL_SIZE, width / 2, height / 2, 1, 0)

    def absolute(x, y) -> Tuple[int, int]:
        return x + offset_x, y + offset_y

    def draw(self):
        pyxel.rect(self.offset_x, self.offset_y, self.width + self.offset_x, self.height + self.offset_y, Color.GRAY.value)


class App:
    x: int = 0
    board: Board

    def __init__(self):
        pyxel.init(WIDTH, HEIGHT)
        self.board = Board(BOARD_WIDTH, BOARD_HEIGHT, PADDING, PADDING)
        pyxel.run(self.update, self.draw)

    def update(self):
        self.x += 1
        self.x = self.x % (WIDTH - 20)

        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        pyxel.cls(Color.BLACK.value)
        self.board.draw()
        pyxel.rect(self.x, self.x, self.x + 1, self.x + 1, Color.GREEN.value)


if __name__ == '__main__':
    Pong()
