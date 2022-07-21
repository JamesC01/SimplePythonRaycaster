import pygame as pg
import math
from pygame import Vector2

class Player:
    FOV = 70
    HALF_FOV = FOV/2
    SPEED = 4
    ROTATE_SPEED = 120

    def __init__(self, pos=Vector2(2,2), angle=45):
        self.pos = pos
        self.angle = angle

    def angle_xy(self):
        """Returns the players current angle degrees as a normalized Vector2"""
        return Vector2(
            math.cos(math.radians(self.angle)),
            math.sin(math.radians(self.angle))
        ).normalize()

    def update(self, delta, map):
        keys = pg.key.get_pressed()

        # Move
        if keys[pg.K_UP]:
            dest = self.pos + self.angle_xy() * Player.SPEED * delta
            if map[int(dest.x)][int(dest.y)] == 0:
                self.pos = dest
        if keys[pg.K_DOWN]:
            dest = self.pos - self.angle_xy() * Player.SPEED * delta
            if map[int(dest.x)][int(dest.y)] == 0:
                    self.pos = dest

        if keys[pg.K_LALT] or keys[pg.K_RALT]:
            right = -Vector2(self.angle_xy(), -self.angle_xy())
            # Strafe
            if keys[pg.K_LEFT]:
                self.pos -= right * Player.SPEED * delta
            if keys[pg.K_RIGHT]:
                self.pos += right * Player.SPEED * delta
        else:
             # Rotate
            if keys[pg.K_LEFT]:
                self.angle -= Player.ROTATE_SPEED * delta
            if keys[pg.K_RIGHT]:
                self.angle += Player.ROTATE_SPEED * delta
