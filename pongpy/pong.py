from logging import getLogger

import pyxel

from pongpy.controllers.board import Board
from pongpy.definitions import PADDING, HEIGHT, WIDTH, BOARD_WIDTH, BOARD_HEIGHT, SET_POINT, MATCH_POINT, FRAME_RATE
from pongpy.interfaces.team import Team
from pongpy.models.color import Color

logger = getLogger(__name__)


class PongMatch:
    team1: Team
    team2: Team
    team1_set_count: int
    team2_set_count: int
    turn: bool

    def __init__(self, team1: Team, team2: Team):
        self.team1 = team1
        self.team2 = team2
        self.team1_set_count = 0
        self.team2_set_count = 0
        self.turn = 1

    def start(self):
        while self.team1_set_count < MATCH_POINT and self.team2_set_count < MATCH_POINT:
            result = {}  # 結果受け渡し用参照オブジェクト
            if self.turn > 0:
                Pong(self.team1, self.team2, result=result)
                if result['win_left']:
                    self.team1_set_count += 1
                else:
                    self.team2_set_count += 1
            else:
                Pong(self.team2, self.team1, result=result)
                if result['win_left']:
                    self.team2_set_count += 1
                else:
                    self.team1_set_count += 1
            self.turn *= -1
        win_team = self.team1 if self.team1_set_count > self.team2_set_count else self.team2
        print(f'Winner: {win_team.name}')


class Pong:
    board: Board
    left_team: Team
    right_team: Team
    result: dict
    turn: bool
    games = []

    def __init__(self, left_team: Team, right_team: Team, result: dict):
        pyxel.init(WIDTH, HEIGHT, fps=FRAME_RATE)
        self.left_team = left_team
        self.right_team = right_team
        self.board = Board(BOARD_WIDTH, BOARD_HEIGHT, PADDING, PADDING, left_team=self.left_team, right_team=self.right_team)
        self.result = result
        pyxel.run(self.update, self.draw)

    def update(self):

        self.board.update()

        # 1ゲーム終了条件
        if self.board.p1.score >= SET_POINT or self.board.p2.score >= SET_POINT:
            print(f'{self.board.p1.score_label} {self.board.p2.score_label}')
            self.result.update({
                'win_left': self.board.p1.score > self.board.p2.score,
                'p1': self.board.p1.score,
                'p2': self.board.p2.score
            })
            pyxel.quit()

    def draw(self):
        pyxel.cls(Color.BLACK.value)
        self.board.draw()
        pyxel.text(PADDING * 2, HEIGHT - PADDING * 2, ''.join('o' if x else 'x' for x in self.games), Color.GRAY.value)
