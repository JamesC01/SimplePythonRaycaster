# A simple pygame raycaster started on 19/07/2022 by James Czekaj
# I enjoyed making this. I used my previous experience from the lodev tutorial, and now a more
# simple tutorial here: https://github.com/vinibiavatti1/RayCastingTutorial
# I simplified some things in that tutorial, and now I believe I finally fully understand how
# a raycaster works.

import pygame, sys, math
from pygame import Vector2

class Player:
    FOV = 60
    HALF_FOV = FOV/2
    SPEED = 4
    ROTATE_SPEED = 180

    def __init__(self, pos=Vector2(2,2), angle=90):
        self.pos = pos
        self.angle = angle

    def update(self):
        keys = pygame.key.get_pressed()

        angle_xy = Vector2(
            math.cos(math.radians(self.angle)),
            math.sin(math.radians(self.angle))
        ).normalize()

        # Move
        if keys[pygame.K_UP]:
            dest = self.pos + angle_xy * Player.SPEED * delta_time
            if map[int(dest.x)][int(dest.y)] == 0:
                self.pos = dest
        if keys[pygame.K_DOWN]:
            dest = self.pos - angle_xy * Player.SPEED * delta_time
            if map[int(dest.x)][int(dest.y)] == 0:
                    self.pos = dest

        # Rotate
        if keys[pygame.K_LEFT]:
            self.angle -= Player.ROTATE_SPEED * delta_time
        if keys[pygame.K_RIGHT]:
            self.angle += Player.ROTATE_SPEED * delta_time


# Size of the raycaster surface
RAYCAST_WIDTH = 320
RAYCAST_HEIGHT = 240
RAYCAST_HALF_WIDTH = RAYCAST_WIDTH/2
RAYCAST_HALF_HEIGHT = RAYCAST_HEIGHT/2

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

increment_angle = Player.FOV / RAYCAST_HEIGHT
precision = 0.1 # ray increment amount

def ceiling_and_floor(floor_color, ceiling_color):
    for y in range(0, int(RAYCAST_HALF_HEIGHT)):
        color = 255-(255*(y/RAYCAST_HALF_HEIGHT+0.0001))
        if color < 0:
            color = 0
        if color > 255:
            color = 255
        pygame.draw.line(raycast_surface, (color*ceiling_color[0], color*ceiling_color[1], color*ceiling_color[2]), (0, y), (RAYCAST_WIDTH, y))
    for y in range(int(RAYCAST_HALF_HEIGHT), int(RAYCAST_HEIGHT)):
        color = 255*((y-RAYCAST_HALF_HEIGHT)/RAYCAST_HALF_HEIGHT+0.0001)
        if color < 0:
            color = 0
        if color > 255:
            color = 255
        pygame.draw.line(raycast_surface, (color*floor_color[0], color*floor_color[1], color*floor_color[2]), (0, y), (RAYCAST_WIDTH, y))

def raycast():
    ray_angle = player.angle - Player.HALF_FOV
    for x in range(0, RAYCAST_WIDTH):
        ray_pos = player.pos.copy()

        ray_dir = Vector2(math.cos(math.radians(ray_angle)),
                         math.sin(math.radians(ray_angle))).normalize()
        
        # Keep moving rayPos along rayDir until it hits a wall
        wall = 0
        while(wall == 0):
            ray_pos += ray_dir * precision
            wall = map[int(ray_pos.x)][int(ray_pos.y)]

        ray_length_xy = player.pos - ray_pos
        distance = ray_length_xy.length()

        wall_height = math.floor(RAYCAST_HEIGHT / distance) * 0.5

        color = 255/distance
        if color < 0:
            color = 0
        if color > 255:
            color = 255

        pygame.draw.line(raycast_surface, (color*0.8, color*0.6, color), (x, RAYCAST_HALF_HEIGHT - wall_height), (x, RAYCAST_HALF_HEIGHT + wall_height))
        ray_angle += increment_angle

pygame.init()
raycast_surface = pygame.surface.Surface((RAYCAST_WIDTH, RAYCAST_HEIGHT))
screen = pygame.display.set_mode((1280, 960))

player = Player()

while True:
    loop_start_time = pygame.time.get_ticks()/1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    player.update()

    ceiling_and_floor((0.2, 0.2, 0.2), (0.3, 0.2, 0.1))
    raycast()

    screen.blit(pygame.transform.scale(raycast_surface, (screen.get_width(), screen.get_height())), (0, 0))
    
    pygame.display.flip()
    
    delta_time = pygame.time.get_ticks()/1000 - loop_start_time
