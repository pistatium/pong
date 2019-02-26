from typing import Tuple, NamedTuple
from enum import Enum
import random

import pyxel


BOARD_WIDTH = 192
BOARD_HEIGHT = 128
PADDING = 3
WIDTH = 192 + PADDING * 2
HEIGHT = 128 + PADDING + 12
BALL_SIZE = 4


class Color(Enum):
    BLACK = 0
    GRAY = 7
    GREEN = 11


class Pos(NamedTuple):
    """ ボード内の相対座標 """
    x: int
    y: int


class BoardInfo(NamedTuple):
    width: int
    height: int


class Team:
    name: str = 'team'

    def atk_update(*args, **kwargs):
        return 2

    def def_pudate(*args, **kwargs):
        return 1


class TeamManager:
    def __init__(self, bi: BoardInfo, team: Team, opposite: bool):
        self.team = team
        if opposite:
            self.atk_pos = Pos(bi.width / 6, bi.height / 2)
            self.atk_pos = Pos(bi.width / 6 * 3, bi.height / 2)
        else:
            self.atk_pos = Pos(bi.width / 6 * 9, bi.height / 2)
            self.atk_pos = Pos(bi.width / 6 * 11, bi.height / 2)

    def update(self):
        atk_action = atk_update(bi)


class Ball:
    size: int
    pos: Pos
    vx: float
    vy: float

    def __init__(self, size: int, pos: Pos, vx: float, vy: float):
        self.size = size
        self.pos = pos
        self.vx = vx
        self.vy = vy

    def updated(self):
        return Pos(self.pos.x + self.vx, self.pos.y + self.vy)

    def __str__(self):
        return f'px: {self.pos.x} py: {self.pos.y} vx: {self.vx} vy: {self.vy}'


class Board:
    p1_score: int = 0
    p2_score: int = 0
    width: int
    height: int
    offset_x: int
    offset_y: int
    ball: Ball

    def __init__(self, width: int, height: int, offset_x: int, offset_y: int):
        self.p1_score = 0
        self.p2_score = 0
        self.width = width
        self.height = height
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.ball = Ball(BALL_SIZE, Pos(width / 2, height / 2), 1, random.random() * 5)

    def absolute(self, pos) -> Tuple[int, int]:
        return pos.x + self.offset_x, pos.y + self.offset_y

    def update(self):
        ball_pos = self.ball.updated()
        self.ball.pos = ball_pos
        if ball_pos.y < 0:
            self.ball.pos = Pos(ball_pos.x, -ball_pos.y)
            self.ball.vy *= -1
        if ball_pos.y > self.height:
            self.ball.pos = Pos(ball_pos.x, self.height - (ball_pos.y - self.height))
            self.ball.vy *= -1
        if ball_pos.x < 0:
            # p2 ゴール
            self.p2_score += 1
            self.ball.pos = Pos(self.width / 2, self.height / 2)
            self.ball.vx = 1
            self.ball.vy = random.random() * 5
        if ball_pos.x > self.width:
            # p1 ゴール
            self.p1_score += 1
            self.ball.pos = Pos(self.width / 2, self.height / 2)
            self.ball.vx = -1
            self.ball.vy = random.random() * 5

    def draw(self):
        pyxel.rect(self.offset_x, self.offset_y, self.width + self.offset_x, self.height + self.offset_y, Color.GRAY.value)
        ball_x, ball_y = self.absolute(self.ball.pos)
        pyxel.rect(ball_x - BALL_SIZE / 2, ball_y - BALL_SIZE / 2, ball_x + BALL_SIZE / 2, ball_y + BALL_SIZE / 2, Color.GREEN.value)


class Pong:
    board: Board

    def __init__(self):
        pyxel.init(WIDTH, HEIGHT)
        self.board = Board(BOARD_WIDTH, BOARD_HEIGHT, PADDING, PADDING)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        self.board.update()

    def draw(self):
        pyxel.cls(Color.BLACK.value)
        self.board.draw()


if __name__ == '__main__':
    Pong()
