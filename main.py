import pyxel

WIDTH = 180
HEIGHT = 120


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
