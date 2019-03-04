# Pong


![](https://raw.githubusercontent.com/pistatium/pong/master/resources/demo.gif)


Python + [pyxel](https://github.com/kitao/pyxel/blob/master/README.ja.md) で作成した Pong ゲームです。

Team を実装して CPU 同士を戦わせる事ができます


## インストール

```sh
$ pip install -U pongpy
```

### 対戦開始

```sh
$ pongpy
```

デフォルトだとプリインストールされたチーム同士で戦います。


## Team を実装する


![](https://raw.githubusercontent.com/pistatium/pong/master/resources/about_pong.png)

pongpy/interfaces/team.py を継承することで独自のチームを作ることが出来ます。

とりあえずサンプルのチームを動かしてみましょう。

```python
from pongpy.interfaces.team import Team
from pongpy.models.game_info import GameInfo
from pongpy.models.state import State


class MyTeam(Team):
    @property
    def name(self) -> str:
        return 'myteam'

    def atk_action(self, info: GameInfo, state: State) -> int:
        return 1

    def def_action(self, info: GameInfo, state: State) -> int:
        return 1

```

のようなスクリプトを myteam.py という名前で作ります。

```sh
$ pongpy myteam:MyTeam
```

のようにコマンドを叩くと、今作ったチームとの対戦が始まります。
