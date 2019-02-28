from logging import getLogger

import pyxel

from pongpy.controllers.board import Board
from pongpy.definitions import PADDING, HEIGHT, WIDTH, BOARD_WIDTH, BOARD_HEIGHT, WIN_POINT, MATCH_POINT
from pongpy.interfaces.team import Team
from pongpy.models.color import Color

logger = getLogger(__name__)


class Pong:
    board: Board
    team1: Team
    team2: Team
    turn: bool
    games = []

    def __init__(self, team1: Team, team2: Team):
        pyxel.init(WIDTH, HEIGHT)
        self.team1 = team1
        self.team2 = team2
        self.turn = True
        self.board = Board(BOARD_WIDTH, BOARD_HEIGHT, PADDING, PADDING, team1=self.team1, team2=self.team2)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.board.update()

        # 1ゲーム終了条件
        if self.board.p1.score >= WIN_POINT or self.board.p2.score >= WIN_POINT:
            print(f'{self.board.p1.score_label} {self.board.p2.score_label}')
            self.games.append(self.board.p1.score > self.board.p2.score)
            if len([x for x in self.games if x]) >= MATCH_POINT:
                print(f'WINNER: {self.team1.name}')
                pyxel.quit()
            if len([x for x in self.games if not x]) >= MATCH_POINT:
                print(f'WINNER: {self.team2.name}')
                pyxel.quit()
            self.turn = not self.turn
            if not self.turn:
                self.board = Board(BOARD_WIDTH, BOARD_HEIGHT, PADDING, PADDING, team1=self.team2, team2=self.team1)
            else:
                self.board = Board(BOARD_WIDTH, BOARD_HEIGHT, PADDING, PADDING, team1=self.team1, team2=self.team2)

    def draw(self):
        pyxel.cls(Color.BLACK.value)
        self.board.draw()
        pyxel.text(PADDING * 2, HEIGHT - PADDING * 2, ''.join('o' if x else 'x' for x in self.games), Color.GRAY.value)


if __name__ == '__main__':
    from pongpy.teams.random_team import RandomTeam
    from pongpy.teams.follow_team import FollowTeam
    Pong(FollowTeam(), RandomTeam())
