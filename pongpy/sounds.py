from enum import Enum
import pyxel

# FIXME: このへんの構造よくわかってない
#   ch: 独立して音楽再生できる空間?
#   sound: 音を登録しておく場所? 
class SoundChannel(Enum):
    SE = 0
    BGM = 1

class Sound(Enum):
    LEFT_POINT = 1
    RIGHT_POINT = 2
    BGM_1 = 30
    BGM_2 = 31
    BGM_3 = 32

class Music(Enum):
    MAIN_BGM = 0

def init_sounds():
    """
    Soundの初期登録をする
    """

    # 左側チームの得点音
    pyxel.sound(Sound.LEFT_POINT.value).set(
        note="c3e3g3c4c4", 
        tone="s", 
        volume="4", 
        effect=("n" * 4 + "f"), 
        speed=5
    )

    # 右側チームの得点音
    pyxel.sound(Sound.RIGHT_POINT.value).set(
        note="f3b2f2b1",
        tone="p",
        volume="4",
        effect=("n" * 7 + "f"),
        speed=5,
    )

    # BGM
    # とりあえずサンプルを拝借
    melody = (
        "rrrr e3e3e3e3 d3d3c3c3 b2b2c3c3"
        + "a2a2a2a2 c3c3c3c3 d3d3d3d3 e3e3e3e3"
        + "rrrr e3e3e3e3 d3d3c3c3 b2b2c3c3"
        + "a2a2a2a2 g2g2g2g2 c3c3c3c3 g2g2a2a2"
        + "rrrr e3e3e3e3 d3d3c3c3 b2b2c3c3"
        + "a2a2a2a2 c3c3c3c3 d3d3d3d3 e3e3e3e3"
        + "f3f3f3a3 a3a3a3a3 g3g3g3b3 b3b3b3b3"
        + "b3b3b3b4 rrrr e3d3c3g3 a2g2e2d2"
    )
    harmony1 = (
        "a1 a1 a1 b1  f1 f1 c2 c2"
        "c2 c2 c2 c2  g1 g1 b1 b1" * 3
        + "f1 f1 f1 f1 f1 f1 f1 f1 g1 g1 g1 g1 g1 g1 g1 g1"
    )

    harmony2 = (
        ("f1" * 8 + "g1" * 8 + "a1" * 8 + ("c2" * 7 + "d2")) * 3 + "f1" * 16 + "g1" * 16
    )

    pyxel.sound(Sound.BGM_2.value).set(
        note=harmony1 * 2 + harmony2 * 2, tone="t", volume="5", effect="f", speed=20
    )
    
    pyxel.sound(Sound.BGM_3.value).set(
        note=("f0 r a4 r  f0 f0 a4 r" "f0 r a4 r   f0 f0 a4 f0"),
        tone="n",
        volume="6622 6622 6622 6426",
        effect="f",
        speed=20,
    )

    pyxel.sound(Sound.BGM_1.value).set(
        note=melody,
        tone="s",
        volume=("3"),
        effect=("nnnsffff"),
        speed=20,
    )

    ch0 = []
    ch1 = [Sound.BGM_1.value, ]
    ch2 = [Sound.BGM_2.value, ]
    ch3 = [Sound.BGM_3.value, ]

    pyxel.music(Music.MAIN_BGM.value).set(ch0, ch1, ch2, ch3)

def play_se(se: Sound):
    pyxel.play(SoundChannel.SE.value, se.value)


def play_bgm():
    pyxel.playm(Music.MAIN_BGM.value, loop=True)

