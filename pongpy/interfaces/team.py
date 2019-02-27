import abc

from pongpy.models.game_info import GameInfo
from pongpy.models.state import State


class Team(metaclass=abc.ABCMeta):

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """
        Team名をセットする
        :return name: 半角英数字、8字以内
         """
        return self.__class__.__name__

    @abc.abstractmethod
    def atk_action(self, info: GameInfo, state: State) -> int:
        """
        atk の行動を決定する
        :param info: ゲーム情報
        :param state: 現在の情報
        :return y: どれくらい動くか -atk_return_limit <= y <= atk_return_limit
        """
        return 0

    def def_action(self, info: GameInfo, state: State) -> int:
        """
        def の行動を決定する
        :param info: ゲーム情報
        :param state: 現在の情報
        :return y: どれくらい動くか -def_return_limit <= y <= def_return_limit
        """
        return 0
