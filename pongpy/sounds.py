from enum import Enum
import pyxel

from pongpy.definitions import ENABLE_SOUND


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
    katyusha_melody1 = (
        'd3d3d3d3 d3d3e3e3 f3f3f3f3 f3f3d3d3'
        + 'f3f3f3f3 e3e3d3d3 e3e3e3e3 a2a2a2a2'
        + 'e3e3e3e3 e3e3f3f3 g3g3g3g3 g3g3e3e3'
        + 'g3g3g3g3 f3f3e3e3 d3d3d3d3 d3d3d3d3'
    )

    katyusha_melody2 = (
        'a3a3a3a3 d4d4d4d4 c4c4c4c4 d4d4c4c4'
        + 'b-3b-3b-3b-3 a3a3g3g3 a3a3a3a3 d3d3d3d3'
        + 'rrb-3b-3 b-3b-3g3g3 a3a3a3a3 a3a3f3f3'
        + 'g3g3g3g3 f3f3e3e3 d3d3d3d3 d3d3d3r'
    )

    katsusha_base_1 = (
        'd2d2a2a2 d2d2a2a2 d2d2a2a2 d2d2a2a2'
        + 'd2d2a2a2 d2d2a2a2 a1a1c#2c#2 a1a1e2e2'
        + 'a1a1c#2c#2 a1a1e2e2 a1a1c#2c#2 a1a1e2e2'
        + 'a1a1e2e2 a1a1e2e2 d2d2a2a2 d2d2a2a2'
    )

    katsusha_base_2 = (
        'b-1b-1f2f2 b-1b-1f2f2 a1a1c#2c#2 a1a1e2e2'
        + 'g1g1d2d2 g1g1b-1b-1 d2d2a2a2 d2d2a2a2'
        + 'g1g1d2d2 g1g1b-1b-1 d2d2a2a2 d2d2a2a2'
        + 'a1a1e2e2 a1a1e2e2 d2d2a2a2 d2d2a2a2'
    )

    katsusha = katyusha_melody1 + katyusha_melody2 * 2
    katsusha_base = katsusha_base_1 + katsusha_base_2 * 2

    pyxel.sound(Sound.BGM_1.value).set(
        note=katsusha,
        tone="s",
        volume=("3"),
        effect=("n"),
        speed=12,
    )

    pyxel.sound(Sound.BGM_2.value).set(
        note=katsusha_base,
        tone="t",
        volume=("2"),
        effect=("n"),
        speed=12,
    )

    ch0 = []
    ch1 = [Sound.BGM_1.value, ]
    ch2 = [Sound.BGM_2.value, ]
    ch3 = [Sound.BGM_3.value, ]

    pyxel.music(Music.MAIN_BGM.value).set(ch0, ch1, ch2, ch3)


def play_se(se: Sound):
    if ENABLE_SOUND:
        pyxel.play(SoundChannel.SE.value, se.value)


def play_bgm():
    if ENABLE_SOUND:
        pyxel.playm(Music.MAIN_BGM.value, loop=True)
