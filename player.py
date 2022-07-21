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
            self.try_move_along_angle(delta, map, 1)

        if keys[pg.K_DOWN]:
            self.try_move_along_angle(delta, map, -1)


        if keys[pg.K_LALT] or keys[pg.K_RALT]:
            right = -Vector2(self.angle_xy().y, -self.angle_xy().x)
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

    def try_move_along_angle(self, delta, map, dir):
        """Attempts to move the player along its forward angle.

            Arguments:
            delta -- delta time
            map -- the map to check for collisions.
            dir -- -1 or 1, corrosponding to back and forward"""
        if dir != -1 and dir != 1:
            raise ValueError('dir needs to be 1 or -1')

        xmotion = self.angle_xy().x * Player.SPEED * delta
        xmotion *= dir
        if map[int(self.pos.x+xmotion)][int(self.pos.y)] == 0:
            self.pos.x += xmotion

        ymotion = self.angle_xy().y * Player.SPEED * delta
        ymotion *= dir
        if map[int(self.pos.x)][int(self.pos.y+ymotion)] == 0:
            self.pos.y += ymotion

