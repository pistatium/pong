import random
from typing import Tuple

import pyxel

from pongpy.controllers.ball import Ball
from pongpy.controllers.team_manager import TeamManager
from pongpy.interfaces.team import Team
from pongpy.models.color import Color
from pongpy.models.game_info import GameInfo
from pongpy.models.pos import Pos
from pongpy.models.state import State
from pongpy.definitions import BALL_SIZE, BAR_WIDTH, ATK_SIZE, DEF_SIZE, PADDING, MAX_VY


class Board:
    game_info: GameInfo
    p1: TeamManager
    p2: TeamManager
    offset_x: int
    offset_y: int
    ball: Ball

    def __init__(self, width: int, height: int, offset_x: int, offset_y: int, left_team: Team, right_team: Team):
        self.game_info = GameInfo(width=width, height=height)
        self.p1 = TeamManager(self.game_info, left_team, reversed=False)
        self.p2 = TeamManager(self.game_info, right_team, reversed=True)
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.ball = Ball(BALL_SIZE, Pos(width // 2, height // 2), 1, random.random() * 5)

    def absolute(self, pos) -> Tuple[int, int]:
        return pos.x + self.offset_x, pos.y + self.offset_y

    def update(self):
        time = pyxel.frame_count
        p1_state = State(is_right_side=False, mine_team=self.p1.state, enemy_team=self.p2.state, ball_pos=self.ball.pos, time=time)
        p2_state = State(is_right_side=True, mine_team=self.p2.state, enemy_team=self.p1.state, ball_pos=self.ball.pos, time=time)
        self.p1.update(p1_state)
        self.p2.update(p2_state)

        ball_pos = self.ball.updated()
        self.ball.pos = ball_pos
        if ball_pos.y <= 0:
            self.ball.pos = Pos(ball_pos.x, -ball_pos.y)
            self.ball.vy *= -1
        if ball_pos.y >= self.game_info.height:
            self.ball.pos = Pos(ball_pos.x, self.game_info.height - (ball_pos.y - self.game_info.height))
            self.ball.vy *= -1
        if ball_pos.x < 0:
            # p2 ゴール
            self.p2.add_score()
            self.ball.pos = Pos(self.game_info.width // 2, self.game_info.height // 2)
            self.ball.vx = 1
            self.ball.vy = random.random() * 2
        if ball_pos.x > self.game_info.width:
            # p1 ゴール
            self.p1.add_score()
            self.ball.pos = Pos(self.game_info.width // 2, self.game_info.height // 2)
            self.ball.vx = -1
            self.ball.vy = random.random() * 2
        for player in (self.p1, self.p2):
            if player.atk_pos.x - BAR_WIDTH // 2 <= ball_pos.x <= player.atk_pos.x + BAR_WIDTH // 2:
                if player.atk_pos.y - ATK_SIZE // 2 <= ball_pos.y <= player.atk_pos.y + ATK_SIZE // 2:
                    self.ball.vx = self.ball.vx * -1
                    diff = ball_pos.y - player.atk_pos.y + (random.random() - 0.5) * 2
                    self.ball.vy += diff
            if player.def_pos.x - BAR_WIDTH // 2 <= ball_pos.x <= player.def_pos.x + BAR_WIDTH // 2:
                if player.def_pos.y - DEF_SIZE // 2 <= ball_pos.y <= player.def_pos.y + DEF_SIZE // 2:
                    self.ball.vx = self.ball.vx * -1
                    diff = ball_pos.y - player.def_pos.y
                    self.ball.vy += diff // 6

        # 最高速度規制
        if self.ball.vy > MAX_VY:
            self.ball.vy = MAX_VY
        if self.ball.vy < -MAX_VY:
            self.ball.vy = -MAX_VY

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
