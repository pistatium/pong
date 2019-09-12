from logging import getLogger

import pyxel

from pongpy.controllers.board import Board
from pongpy.definitions import PADDING, HEIGHT, WIDTH, BOARD_WIDTH, BOARD_HEIGHT, SET_POINT, FRAME_RATE
from pongpy.interfaces.team import Team
from pongpy.models.color import Color
from pongpy.sounds import play_bgm, init_sounds

logger = getLogger(__name__)


class Game:
    team1: Team
    team2: Team

    def __init__(self, team1: Team, team2: Team):
        self.team1 = team1
        self.team2 = team2

    def start(self):
        Pong(self.team1, self.team2)


class Pong:
    board: Board
    left_team: Team
    right_team: Team
    result: dict
    turn: bool
    games = []

    def __init__(self, left_team: Team, right_team: Team):
        pyxel.init(WIDTH, HEIGHT, fps=FRAME_RATE)
        init_sounds()
        self.left_team = left_team
        self.right_team = right_team
        self.board = Board(BOARD_WIDTH, BOARD_HEIGHT, PADDING, PADDING, left_team=self.left_team, right_team=self.right_team)

        play_bgm()
        pyxel.run(self.update, self.draw)

    def update(self):

        self.board.update()

        # ゲーム終了条件
        if self.board.p1.score >= SET_POINT or self.board.p2.score >= SET_POINT:
            # デュース判定
            if abs(self.board.p1.score - self.board.p2.score) >= 2:
                print(f'{self.board.p1.score_label} {self.board.p2.score_label}')
                # 最新のPyxel だと quit したときに Python 自体 exit してしまう
                pyxel.quit()

    def draw(self):
        pyxel.cls(Color.BLACK.value)
        self.board.draw()
        pyxel.text(PADDING * 2, HEIGHT - PADDING * 2, ''.join('o' if x else 'x' for x in self.games), Color.GRAY.value)
