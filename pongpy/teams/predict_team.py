from pongpy.interfaces.team import Team
from pongpy.models.game_info import GameInfo
from pongpy.models.state import State
from pongpy.models.pos import Pos


class PredictTeam(Team):

    prev_ball: Pos

    @property
    def name(self) -> str:
        return 'Predict'

    def __init__(self):
        self.prev_ball = Pos(0, 0)

    def atk_action(self, info: GameInfo, state: State) -> int:

        diff_x = state.mine_team.atk_pos.x - state.ball_pos.x
        vec_y = state.ball_pos.y - self.prev_ball.y
        total_y = vec_y * diff_x
        if total_y // info.height % 2 == 1:
            return self.aim_to(state.mine_team.atk_pos, total_y % info.height) * info.atk_return_limit
        else:
            return self.aim_to(state.mine_team.atk_pos, info.height - total_y % info.height) * info.atk_return_limit

    def def_action(self, info: GameInfo, state: State) -> int:
        diff_x = state.mine_team.def_pos.x - state.ball_pos.x
        vec_y = state.ball_pos.y - self.prev_ball.y
        total_y = vec_y * diff_x

        self.prev_ball = state.ball_pos

        if total_y // info.height % 2 == 0:
            return self.aim_to(state.mine_team.def_pos, total_y % info.height) * info.def_return_limit
        else:
            return self.aim_to(state.mine_team.def_pos, info.height - total_y % info.height) * info.def_return_limit

    def aim_to(self, current_pos: Pos, target_y: int):
        diff = target_y - current_pos.y
        if diff > 0:
            return 1
        return -1
