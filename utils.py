import pygame as pg
import math


def clamp(val, minval, maxval):
    if val < minval:
        return minval
    elif val > maxval:
        return maxval
    else:
        return val


def degrees_to_vec2(angle) -> pg.Vector2:
    '''Takes an angle in degrees and returns it as a Vector2.'''
    return pg.Vector2(math.cos(math.radians(angle)),
                      math.sin(math.radians(angle)))
