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
ATK_SIZE = 16
DEF_SIZE = 48
ATK_DELTA_LIMIT = 2
DEF_DELTA_LIMIT = 1
BAR_WIDTH = 2


class Color(Enum):
    BLACK = 0
    GRAY = 7
    YELLO = 9
    GREEN = 11
    BLUE = 12


class Pos(NamedTuple):
    """ ボード内の相対座標 """
    x: int
    y: int


class GameInfo(NamedTuple):
    width: int
    height: int
    ball_size = BALL_SIZE
    atk_size = ATK_SIZE
    atk_return_limit = ATK_DELTA_LIMIT
    def_size = DEF_SIZE
    def_return_limit = DEF_DELTA_LIMIT
    bar_width = BAR_WIDTH


class TeamState(NamedTuple):
    atk_pos: Pos
    def_pos: Pos
    score: int


class State(NamedTuple):
    reversed: bool
    mine_team: TeamState
    enemy_team: TeamState
    ball_pos: Pos


class Team:
    """ これを継承してロジックを作る """
    name: str = 'team'

    atk_reversed = 1
    def_reversed = 1

    def atk_update(self, info: GameInfo, state: State) -> int:
        if random.random() > 0.9:
            self.atk_reversed *= -1
        return 2 * self.atk_reversed

    def def_pudate(self, info: GameInfo, state: State) -> int:
        if random.random() > 0.95:
            self.def_reversed *= -1
        return 1 * self.def_reversed


class TeamManager:
    game_info: GameInfo
    atk_pos: Pos
    def_pos: Pos
    score: int

    def __init__(self, gi: GameInfo, team: Team, reversed: bool):
        self.team = team
        self.game_info = gi
        self.score = 0
        if reversed:
            self.atk_pos = Pos(gi.width // 12 * 5, gi.height // 2)
            self.def_pos = Pos(gi.width // 12 * 1, gi.height // 2)
        else:
            self.atk_pos = Pos(gi.width // 12 * 7, gi.height // 2)
            self.def_pos = Pos(gi.width // 12 * 11, gi.height // 2)

    def update(self, state: State):
        atk_action = self.team.atk_update(info=self.game_info, state=state)
        assert -self.game_info.atk_return_limit <= atk_action <= self.game_info.atk_return_limit, 'atk の返り値が大きすぎます'
        self.atk_pos = Pos(self.atk_pos.x, self._move_y(atk_action, self.atk_pos, ATK_SIZE))
        def_action = self.team.def_pudate(info=self.game_info, state=state)
        assert -self.game_info.def_return_limit <= def_action <= self.game_info.def_return_limit, 'def の返り値が大きすぎます'
        self.def_pos = Pos(self.def_pos.x, self._move_y(def_action, self.def_pos, DEF_SIZE))

    def add_score(self):
        self.score += 1

    def _move_y(self, y_delta: float, pos: Pos, size: int) -> int:
        if y_delta + pos.y - size // 2 < 0:
            return 0 + size // 2
        if y_delta + pos.y + size // 2 > self.game_info.height:
            return self.game_info.height - size // 2
        return int(y_delta + pos.y)

    @property
    def state(self) -> TeamState:
        return TeamState(atk_pos=self.atk_pos, def_pos=self.def_pos, score=self.score)

    @property
    def score_label(self) -> str:
        return f'{self.team.name}: {self.score}'


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
    game_info: GameInfo
    p1: TeamManager
    p2: TeamManager
    offset_x: int
    offset_y: int
    ball: Ball

    def __init__(self, width: int, height: int, offset_x: int, offset_y: int):
        self.game_info = GameInfo(width=width, height=height)
        self.p1 = TeamManager(self.game_info, Team(), reversed=False)
        self.p2 = TeamManager(self.game_info, Team(), reversed=True)
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.ball = Ball(BALL_SIZE, Pos(width // 2, height // 2), 1, random.random() * 5)

    def absolute(self, pos) -> Tuple[int, int]:
        return pos.x + self.offset_x, pos.y + self.offset_y

    def update(self):
        p1_state = State(reversed=False, mine_team=self.p1.state, enemy_team=self.p2.state, ball_pos=self.ball.pos)
        p2_state = State(reversed=True, mine_team=self.p2.state, enemy_team=self.p1.state, ball_pos=self.ball.pos)
        self.p1.update(p1_state)
        self.p2.update(p2_state)

        ball_pos = self.ball.updated()
        self.ball.pos = ball_pos
        if ball_pos.y < 0:
            self.ball.pos = Pos(ball_pos.x, -ball_pos.y)
            self.ball.vy *= -1
        if ball_pos.y > self.game_info.height:
            self.ball.pos = Pos(ball_pos.x, self.game_info.height - (ball_pos.y - self.game_info.height))
            self.ball.vy *= -1
        if ball_pos.x < 0:
            # p2 ゴール
            self.p2.add_score()
            self.ball.pos = Pos(self.game_info.width // 2, self.game_info.height // 2)
            self.ball.vx = 1
            self.ball.vy = random.random() * 5
        if ball_pos.x > self.game_info.width:
            # p1 ゴール
            self.p1.add_score()
            self.ball.pos = Pos(self.game_info.width // 2, self.game_info.height // 2)
            self.ball.vx = -1
            self.ball.vy = random.random() * 5
        for player in (self.p1, self.p2):
            if player.atk_pos.x - BAR_WIDTH // 2 <= ball_pos.x <= player.atk_pos.x + BAR_WIDTH // 2:
                if player.atk_pos.y - ATK_SIZE // 2 <= ball_pos.y <= player.atk_pos.y + ATK_SIZE // 2:
                    self.ball.vx = self.ball.vx * -1
                    diff = ball_pos.y - player.atk_pos.y
                    self.ball.vy += diff
            if player.def_pos.x - BAR_WIDTH // 2 <= ball_pos.x <= player.def_pos.x + BAR_WIDTH // 2:
                if player.def_pos.y - DEF_SIZE // 2 <= ball_pos.y <= player.def_pos.y + DEF_SIZE // 2:
                    self.ball.vx = self.ball.vx * -1
                    diff = ball_pos.y - player.def_pos.y
                    self.ball.vy += diff // 5

    def draw(self):
        pyxel.rect(
            self.offset_x,
            self.offset_y,
            self.game_info.width + self.offset_x,
            self.game_info.height + self.offset_y,
            Color.GRAY.value)

        ball_x, ball_y = self.absolute(self.ball.pos)
        pyxel.rect(
            ball_x - BALL_SIZE // 2,
            ball_y - BALL_SIZE // 2,
            ball_x + BALL_SIZE // 2,
            ball_y + BALL_SIZE // 2,
            Color.GREEN.value)

        for player in (self.p1, self.p2):
            x, y = self.absolute(player.atk_pos)
            pyxel.rect(
                x - BAR_WIDTH // 2,
                y - ATK_SIZE // 2,
                x + BAR_WIDTH // 2,
                y + ATK_SIZE // 2,
                Color.BLUE.value)

            x, y = self.absolute(player.def_pos)
            pyxel.rect(
                x - BAR_WIDTH // 2,
                y - DEF_SIZE // 2,
                x + BAR_WIDTH // 2,
                y + DEF_SIZE // 2,
                Color.YELLO.value)
        x, y = self.absolute(Pos(0, self.game_info.height))
        scores = f'{self.p1.score_label} {self.p2.score_label}'
        pyxel.text(x + PADDING, y + PADDING, scores, Color.GRAY.value)


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
