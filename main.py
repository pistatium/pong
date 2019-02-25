from typing import Tuple

import pyxel


WIDTH = 180
HEIGHT = 120
BALL_SIZE = 4
FRICTION = 0.95


class Obj:
    size: int
    friction: float
    x: int
    y: int
    vx: float
    vy: float

    def __init__(self, size: int, friction: float, x: int, y: int):
        self.size = size
        self.friction = friction
        self.x = x
        self.y = y
        self.vx = 0.0
        self.vy = 0.0

    def add_force(ax: float, ay: float):
        self.vx += ax
        self.vy += ay

    def updated() -> :
        self.x += self.vx
        self.y += self.vy
        self.vx *= self.friction
        self.vy *= self.friction


class Pong:
    x: int = 0

    def __init__(self):
        pyxel.init(WIDTH, HEIGHT)
        self.x = 0
        pyxel.run(self.update, self.draw)

    def update(self):
        self.x += 1
        self.x = self.x % (WIDTH - 20)

        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        pyxel.cls(0)
        pyxel.rect(self.x, self.x, self.x + 20, self.x + 20, 11)
        pass

if __name__ == '__main__':
    Pong()
