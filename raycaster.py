# A simple pygame raycaster made on 19/07/2022 by James Czekaj
# I enjoyed making this. I used my previous experience from the lodev tutorial, and now a more
# simple tutorial here: https://github.com/vinibiavatti1/RayCastingTutorial
# I simplified some things in that tutorial, and now I believe I finally fully understand how
# a raycaster works.

import pygame, sys, math
from pygame import Vector2

class Player:
    fov = 60
    half_fov = fov/2
    pos = Vector2(2,2)
    angle = 90

    SPEED = 4
    ROT_SPEED = 180

    @classmethod
    def update(cls):
        keys = pygame.key.get_pressed()

        angle_vec = Vector2(
            math.cos(math.radians(Player.angle)),
            math.sin(math.radians(Player.angle))
        ).normalize()

        if keys[pygame.K_UP]:
            dest = Player.pos + angle_vec * Player.SPEED * delta_time
            if map[int(dest.x)][int(dest.y)] == 0:
                Player.pos = dest
        if keys[pygame.K_DOWN]:
            dest = Player.pos - angle_vec * Player.SPEED * delta_time
            if map[int(dest.x)][int(dest.y)] == 0:
                    Player.pos = dest
        if keys[pygame.K_LEFT]:
            Player.angle -= Player.ROT_SPEED * delta_time
        if keys[pygame.K_RIGHT]:
            Player.angle += Player.ROT_SPEED * delta_time



RAYCAST_WIDTH = 320
RAYCAST_HEIGHT = 240
RAYCAST_HALF_WIDTH = RAYCAST_WIDTH/2
RAYCAST_HALF_HEIGHT = RAYCAST_HEIGHT/2

increment_angle = Player.fov / RAYCAST_HEIGHT
precision = 0.1 # ray increment amount

map = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

raycast_surface = pygame.surface.Surface((RAYCAST_WIDTH, RAYCAST_HEIGHT))
screen = pygame.display.set_mode((1280, 960))

def ceiling_and_floor():
    for y in range(0, int(RAYCAST_HALF_HEIGHT)):
        color = 255-(255*(y/RAYCAST_HALF_HEIGHT+0.0001))
        if color < 0:
            color = 0
        if color > 255:
            color = 255
        pygame.draw.line(raycast_surface, (color*0.1, color*0.5, color*0.5), (0, y), (RAYCAST_WIDTH, y))
    for y in range(int(RAYCAST_HALF_HEIGHT), int(RAYCAST_HEIGHT)):
        color = 255*((y-RAYCAST_HALF_HEIGHT)/RAYCAST_HALF_HEIGHT+0.0001)
        if color < 0:
            color = 0
        if color > 255:
            color = 255
        pygame.draw.line(raycast_surface, (color*0.1, color*0.4, color*0.8), (0, y), (RAYCAST_WIDTH, y))

def raycast():
    rayAngle = Player.angle - Player.half_fov
    for x in range(0, RAYCAST_WIDTH):
        rayPos = Player.pos.copy()

        rayDir = Vector2(math.cos(math.radians(rayAngle)),
                         math.sin(math.radians(rayAngle))).normalize()
        
        wall = 0
        while(wall == 0):
            rayPos += rayDir * precision
            wall = map[int(rayPos.x)][int(rayPos.y)]

        difference = Player.pos - rayPos
        distance = difference.length()

        wallHeight = math.floor(RAYCAST_HEIGHT / distance) * 0.5

        color = 255/distance
        if color < 0:
            color = 0
        if color > 255:
            color = 255

        pygame.draw.line(raycast_surface, (color*0.8, color*0.6, color), (x, RAYCAST_HALF_HEIGHT - wallHeight), (x, RAYCAST_HALF_HEIGHT + wallHeight))
        rayAngle += increment_angle

pygame.init()

while True:
    loop_start_time = pygame.time.get_ticks()/1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    Player.update()

    ceiling_and_floor()
    raycast()

    screen.blit(pygame.transform.scale(raycast_surface, (screen.get_width(), screen.get_height())), (0, 0))
    
    pygame.display.flip()
    
    delta_time = pygame.time.get_ticks()/1000 - loop_start_time
