# PongPy

![](https://raw.githubusercontent.com/pistatium/pong/master/resources/demo.gif)


Python + [pyxel](https://github.com/kitao/pyxel/blob/master/README.ja.md) で作成した Pong ゲームです。

Team のアルゴリズムを実装することで Team 同士の自動対戦が出来るようになってます。

アルゴリズムの腕試しに挑戦してみてください。



### ゲーム概要

![](https://raw.githubusercontent.com/pistatium/pong/master/resources/about_pong.png)

ベースは Pong と呼ばれるゲームを踏襲しています。

お互いにボールを弾きあい、画面端の相手のゴールへ入れると得点になります。

各チームには アタッカー(ATK) とディフェンダー(DEF) が 1つづついて、前衛と後衛をそれぞれ担当します。

ATK と DEF にはそれぞれ以下の特徴があります。

* ATK: 
   * 幅が狭い
   * 移動速度が早い
   * ボールを跳ね返すとき、斜めに跳ね返しやすい
* DEF:
   * 幅が広い
   * 移動速度が遅い
   * ボールを跳ね返すとき、角度がつきにくい
   
 これらの特徴を生かして、いかに相手のゴールへボールを運べるかを競います。
 
ゲームは 11 点先取したほうが勝利となります。
但しデュースがあるため、2 点以上点差がない場合は差がつくまで続行となります。

また、ラリーが終わらなくなってしまうため、一定時間が経つごとにお互いのATK、DEFが中央側へ近づいていく仕組みがあります。


## インストール

__Requirements__
* Python3.7+
* pyxel
  * インストール方法はリンク先を参照してください
  * Windows / Mac / Linux 対応です
  * https://github.com/kitao/pyxel/blob/master/README.ja.md

__Install__
```sh
$ pip3 install -U pongpy
```

### 対戦開始

```sh
$ pongpy
```

デフォルトだとプリインストールされたチーム同士で戦います。
後述するオプションを指定することで対戦するチームを変更できます。


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
        return 'myteam'  # チーム名(ascii only)

    def atk_action(self, info: GameInfo, state: State) -> int:
        # 毎フレーム、下方向に 2 動く
        return 2

    def def_action(self, info: GameInfo, state: State) -> int:
        # 毎フレーム、上方向に 1 動く
        return -1

```

のようなスクリプトを作ります。 説明のため myteam.py というファイル名でカレントディレクトリに作ります。(好きに変えても大丈夫です)

```sh
$ pongpy myteam:MyTeam
```

のようにコマンドを叩くと、今作ったチームとの対戦が始まります。

※ `ModuleNotFoundError: No module named` というエラーが出てしまう場合は `export PYTHONPATH=$PYTHONPATH:$(pwd)` などで現在のディレクトリをパスとして認識するようにしてみてください。


第二引数では対戦相手を指定できるため、同じチーム同士の対戦も可能です。
第一引数で渡したチームが左側、第二引数で渡したチームが右側で戦います。

```sh
$ pongpy myteam:MyTeam myteam:MyTeam
```

### チームの実装方法
先程の例のように Team インターフェースを実装することでチームの動きを制御できます。
必要なプロパティ・メソッドは以下の3つです。

__name__

チーム名を返すプロパティです。長すぎない ASCII文字列 を返してください。

__def atk_action(self, info: GameInfo, state: State) -> int__

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


__def def_action(self, info: GameInfo, state: State) -> int__

同様に DEF がどう動くかを決めるための関数がこちらです。
範囲は `-DEF_DELTA_LIMIT<= y <= DEF_DELTA_LIMIT` になります。


__その他__

* チームのコンストラクタは引数なしで呼ばれます。
    * 1度だけ実行したい処理があればコンストラクタで実施してください。
* Team インスタンス内に自由に変数等をもたせて構いません。
* Pos の座標は左上隅が (0, 0), 左下が (0, height), 右上が(width, 0) になります。 
* 右側のチームの場合ゴールの向きに注意してください。
    * 自動的な座標変換は行われません。
    * メソッドに渡される情報を見て判断してください。

* チームの参考実装はこちらで見れます。
    * https://github.com/pistatium/pong/tree/master/pongpy/teams


### 実装する上でのレギュレーション
* Team の各関数内から例外をスローしてはいけません
* Team 内で pyxel のインポートや操作をしてはいけません
* ゲーム進行を阻害しない程度の実行時間で結果を返してください
* ゲームに関係ない処理を入れないでください

## FAQ

### BGM、SEを有効にしたい

`export PONGPY_SOUND=1` でゲームの音楽が有効になります。

BGM: Powered by [@TatchNicolas](https://github.com/TatchNicolas)

### 人間 VS CPU で戦ってみたい

`pongpy.teams.manual_team:ManualTeam` をチームとして読み込むとキーボードで動かせます。
「I」「K」「W」「S」 で操作してください。人間 VS 人間は実装してません。

### 設定を変更したい

definitions にある値は環境変数を指定することで変更できます。

### 強いチームを作りたい
前回関数が呼ばれたときのボールの位置をインスタンス変数に保存しておいて、ボールがどう動くかを予測してみましょう。  
到達予定地にATKやDEFが先回りできればかなり強くなります！  

DQNなどの機械学習的なアプローチも挑戦してみてください。

### 物理法則がおかしい

~当たり判定の実装が大変なので~ 横方向の移動距離は一定にしてます。

ボールが斜めに動くほど早く動きますが仕様です。

