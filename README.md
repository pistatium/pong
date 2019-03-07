# Pong

![](https://raw.githubusercontent.com/pistatium/pong/master/resources/demo.gif)


Python + [pyxel](https://github.com/kitao/pyxel/blob/master/README.ja.md) で作成した Pong ゲームです。

Team を実装して CPU 同士を戦わせる事ができます


### ゲーム概要

![](https://raw.githubusercontent.com/pistatium/pong/master/resources/about_pong.png)

各チームには アタッカー(ATK) とディフェンダー(DEF) がいて、前衛と後衛をそれぞれ担当します。

ATK と DEF にはそれぞれ以下の特徴があります。

* ATK: 
   * 縦幅が狭い
   * 動きが早い
   * ボールを跳ね返すとき、斜めに跳ね返しやすい
* DEF:
   * 縦幅が広い
   * 動きが遅い
   * ボールを跳ね返すとき、角度がつきにくい
   
 これらの特徴を生かして、いかに相手のゴールへボールを運べるかを競います。
 
* ゲームは 1セット 5点先取制で、都度左右交換、2セット先取で勝利となります。
* 一定時間が経つとお互いのATK、DEFが近づいていきます。


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

### 動かし方

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

のようなスクリプトを myteam.py という名前で作ります。(好きに変えても大丈夫です)

```sh
$ pongpy myteam:MyTeam
```

のようにコマンドを叩くと、今作ったチームとの対戦が始まります。

第二引数では対戦相手を指定できるため、自分対自分の対戦も可能です。

```sh
$ pongpy myteam:MyTeam myteam:MyTeam
```

### チームの実装方法
先程の例のように Team インターフェースを実装する形でチームの動きを制御します。

__name__

チーム名を返すプロパティです。長すぎない ASCII文字列 を返してください。**

__atk_action__

ATK がどう動くかを決めるための関数です。毎フレームごとに呼び出されます。
ゲーム自体の情報やボール、味方、相手の位置などの情報は引数に入っています。
この引数を見てどのように動かすかを決定します。

返り値にどれくらい縦に移動するかをintで返します。この値の取れる範囲は 
`-ATK_DELTA_LIMIT <= y <= ATK_DELTA_LIMIT` だけになります。
`ATK_DELTA_LIMIT` は引数のinfoの中から参照できます。


| 引数 | 説明 |
----|---- 
| info: GameInfo | ゲーム自体のパラメータが格納されてます https://github.com/pistatium/pong/blob/master/pongpy/models/game_info.py |
| state: State | 現在のゲーム状況が格納されてます https://github.com/pistatium/pong/blob/master/pongpy/models/state.py |


__def_action__

同様に DEF がどう動くかを決めるための関数がこちらです。
範囲は `-DEF_DELTA_LIMIT<= y <= DEF_DELTA_LIMIT` になります。


__その他__

Team クラスは1セットの初めごとに1回初期化されます。
コンストラクタは引数なしで呼ばれます。
Team 内に自由にインスタンス変数して構いませんが、セットをまたいでの変数の保持はできません。
また、自動的な座標変換は行われないので、自分が左右どちらのチームなのかは引数で確認してください。

### ふわっとしたレギュレーション
* Team の各関数内から例外をスローしてはいけません
* Team 内で pyxel のインポートや操作をしてはいけません
* ゲーム進行を阻害しない程度の実行時間で関数は結果を返してください
* ゲームに関係ない処理を入れないでください

## FAQ

### 人間 VS CPU で戦いたい

`pongpy.teams.manual_team:ManualTeam` を読み込むとキーボードで動くようになります。
「I」「K」「W」「S」 で操作してください。人間 VS 人間は実装してません。

### 設定を変更したい

definitions にある値は環境変数を指定することで変更できます。

### 物理法則がおかしい

~当たり判定の実装が大変なので~ 横方向の移動距離は一定にしてます。

ボールが斜めに動くほど早く動きますが仕様です。

