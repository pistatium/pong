from os import environ
BOARD_WIDTH = int(environ.get('PONGPY_BOARD_WIDTH', 192))  # PONGの横幅
BOARD_HEIGHT = int(environ.get('PONGPY_BOARD_HEIGHT', 128))  # PONGの縦幅
PADDING = int(environ.get('PONGPY_PADDING', 3))  # 余白サイズ
TEXT_SIZE = int(environ.get('PONGPY_TEXT_SIZE', 16))
WIDTH = BOARD_WIDTH + PADDING * 2  # 画面横幅
HEIGHT = BOARD_HEIGHT + PADDING + TEXT_SIZE  # 画面縦幅

BALL_SIZE = int(environ.get('PONGPY_BALL_SIZE', 4))  # Ball の大きさ
ATK_SIZE = int(environ.get('PONGPY_ATK_SIZE', 8))  # ATK bar の長さ
DEF_SIZE = int(environ.get('PONGPY_DEF_SIZE', 24))  # DEF bar の長さ
MAX_VY = int(environ.get('MAX_VY', 8))  # ボールの縦方向の最大速度
ATK_DELTA_LIMIT = int(environ.get('PONGPY_ATK_DELTA_LIMIT', 2))  # ATK の移動制限
DEF_DELTA_LIMIT = int(environ.get('PONGPY_DEF_DELTA_LIMIT', 1))  # DEF の移動制限
BAR_WIDTH = int(environ.get('PONGPY_BAR_WIDTH', 2))  # bar の横幅
SET_POINT = int(environ.get('PONGPY_SET_POINT', 5))  # 1ゲームの勝利点
MATCH_POINT = int(environ.get('PONGPY_MATCH_POINT', 2))  # 何ゲーム先取で勝利か
FRAME_RATE = int(environ.get('PONGPY_FRAME_RATE', 100))  # FPS
