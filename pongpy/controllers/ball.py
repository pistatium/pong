from pongpy.models.pos import Pos


class Ball:
    size: int
    pos: Pos
    vx: float
    vy: float

    def __init__(self, size: int, pos: Pos, vx: float, vy: float):
        self.size = size
        self.pos = pos
        self.vx = vx
        self.vy = vy

    def updated(self):
        return Pos(self.pos.x + self.vx, self.pos.y + self.vy)

    def __str__(self):
        return f'px: {self.pos.x} py: {self.pos.y} vx: {self.vx} vy: {self.vy}'
