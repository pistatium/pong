from pongpy.definitions import ATK_SIZE, DEF_SIZE
from pongpy.interfaces.team import Team
from pongpy.models.game_info import GameInfo
from pongpy.models.pos import Pos
from pongpy.models.state import State, TeamState


class TeamManager:
    game_info: GameInfo
    atk_pos: Pos
    def_pos: Pos
    score: int

    def __init__(self, gi: GameInfo, team: Team, reversed: bool):
        self.team = team
        self.game_info = gi
        self.score = 0
        if not reversed:
            self.atk_pos = Pos(gi.width // 12 * 5, gi.height // 2)
            self.def_pos = Pos(gi.width // 12 * 1, gi.height // 2)
        else:
            self.atk_pos = Pos(gi.width // 12 * 7, gi.height // 2)
            self.def_pos = Pos(gi.width // 12 * 11, gi.height // 2)

    def update(self, state: State):
        atk_action = self.team.atk_action(info=self.game_info, state=state)
        assert -self.game_info.atk_return_limit <= atk_action <= self.game_info.atk_return_limit, 'atk の返り値が大きすぎます'
        self.atk_pos = Pos(self.atk_pos.x, self._move_y(atk_action, self.atk_pos, ATK_SIZE))
        def_action = self.team.def_action(info=self.game_info, state=state)
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
