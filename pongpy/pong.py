from logging import getLogger

import pyxel

from pongpy.controllers.board import Board
from pongpy.definitions import PADDING, HEIGHT, WIDTH, BOARD_WIDTH, BOARD_HEIGHT, SET_POINT, MATCH_POINT
from pongpy.interfaces.team import Team
from pongpy.models.color import Color

logger = getLogger(__name__)


class PongMatch:
    team1: Team
    team2: Team
    team1_set_count: int
    team2_set_count: int

    def __init__(self, team1: Team, team2: Team):
        self.team1 = team1
        self.team2 = team2
        self.team1_set_count = 0
        self.team2_set_count = 0

    def update(self):
        pass


class Pong:
    board: Board
    left_team: Team
    right_team: Team
    turn: bool
    games = []

    def __init__(self, left_team: Team, right_team: Team):
        pyxel.init(WIDTH, HEIGHT)
        self.left_team = left_team
        self.right_team = right_team
        self.board = Board(BOARD_WIDTH, BOARD_HEIGHT, PADDING, PADDING, team1=self.left_team, team2=self.right_team)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.board.update()

        # 1ゲーム終了条件
        if self.board.p1.score >= SET_POINT or self.board.p2.score >= SET_POINT:

            print(f'{self.board.p1.score_label} {self.board.p2.score_label}')
            self.games.append(self.board.p1.score > self.board.p2.score)
            if len([x for x in self.games if x]) >= MATCH_POINT:
                print(f'WINNER: {self.left_team.name}')
                pyxel.quit()
            if len([x for x in self.games if not x]) >= MATCH_POINT:
                print(f'WINNER: {self.right_team.name}')
                pyxel.quit()
            self.turn = not self.turn
            if not self.turn:
                self.board = Board(BOARD_WIDTH, BOARD_HEIGHT, PADDING, PADDING, team1=self.right_team, team2=self.left_team)
            else:
                self.board = Board(BOARD_WIDTH, BOARD_HEIGHT, PADDING, PADDING, team1=self.left_team, team2=self.right_team)

    def draw(self):
        pyxel.cls(Color.BLACK.value)
        self.board.draw()
        pyxel.text(PADDING * 2, HEIGHT - PADDING * 2, ''.join('o' if x else 'x' for x in self.games), Color.GRAY.value)
