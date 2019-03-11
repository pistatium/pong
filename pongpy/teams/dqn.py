import pyxel

from pongpy.interfaces.team import Team
from pongpy.models.game_info import GameInfo
from pongpy.models.state import State


class DqnTeam(Team):
    """ デバッグ用、手動操作チーム """
    @property
    def name(self) -> str:
        return 'dqn'

    def atk_action(self, info: GameInfo, state: State) -> int:
        if pyxel._app._capture_images[0]:
            print(pyxel._app._get_capture_image(0))
            print(state.mine_team.score)
            print(state.enemy_team.score)
        if pyxel.btn(pyxel.KEY_I):
            return -info.atk_return_limit
        if pyxel.btn(pyxel.KEY_K):
            return info.atk_return_limit
        return 0

    def def_action(self, info: GameInfo, state: State) -> int:
        if pyxel.btn(pyxel.KEY_W):
            return -info.def_return_limit
        if pyxel.btn(pyxel.KEY_S):
            return info.def_return_limit
        return 0
