import abc

from pongpy.models.game_info import GameInfo
from pongpy.models.state import State


class Team(metaclass=abc.ABCMeta):
    """
    チームを作るためのインターフェース。
    これを継承して自チームを作ってください。
    """

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """
        Team名を返す関数
        :return name: 半角英数字、16字以内
         """
        return self.__class__.__name__

    @abc.abstractmethod
    def atk_action(self, info: GameInfo, state: State) -> int:
        """
        毎フレームの atk の行動を決定する関数。

        :param info: ゲームに関する設定値が入っているオブジェクト
        :param state: ボールや自機の位置など現在のステータスが入っているオブジェクト
        :return y: 縦方向にどれくらい動くか -atk_return_limit <= y <= atk_return_limit
        """
        return 0

    def def_action(self, info: GameInfo, state: State) -> int:
        """
        毎フレームの def の行動を決定する関数。

        :param info: ゲームに関する設定値が入っているオブジェクト
        :param state: ボールや自機の位置など現在のステータスが入っているオブジェクト
        :return y: 縦方向にどれくらい動くか -def_return_limit <= y <= def_return_limit
        """
        return 0
