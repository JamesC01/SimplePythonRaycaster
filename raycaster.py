# A simple pygame raycaster started on 19/07/2022 by James Czekaj
# I enjoyed making this. I used my previous experience from the lodev tutorial, and now a more
# simple tutorial here: https://github.com/vinibiavatti1/RayCastingTutorial
# I simplified some things in that tutorial, and now I believe I finally fully understand how
# a raycaster works.

from doctest import REPORT_CDIFF
import random
import pygame, sys, math
from pygame import Vector2
import opensimplex

class Player:
    FOV = 60
    HALF_FOV = FOV/2
    SPEED = 4
    ROTATE_SPEED = 180

    def __init__(self, pos=Vector2(2,2), angle=45):
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

        # Reposition
        if keys[pygame.K_r]:
            self.reposition()

        if keys[pygame.K_SPACE]:
            ray = self.pos.copy()
            wall = 0
            while wall == 0:
                ray += angle_xy * precision
                wall = map[int(ray.x)][int(ray.y)]
            if wall == 2:
                map[int(ray.x)][int(ray.y)] = 0


    # broken!
    def reposition(self):
        for x in range(100):
            for y in range(100):
                if map[x][y] == 0:
                    self.pos.x = x
                    self.pos.y = y
                    print('break')
                    break
            else:
                break


# Size of the raycaster surface
RAYCAST_WIDTH = 320
RAYCAST_HEIGHT = 240
RAYCAST_HALF_WIDTH = RAYCAST_WIDTH/2
RAYCAST_HALF_HEIGHT = RAYCAST_HEIGHT/2

map = []

increment_angle = Player.FOV / RAYCAST_HEIGHT
precision = 0.1 # ray increment amount

def generate_map(map_size, noise_scale):
    """Generates a 2d list of map_size width and height using simplex noise.
        Also makes sure map boundaries are always walls.
        
        Arguments:
        map_size -- The width and height of the list
        noise_scale -- the scale of the simplex noise (smaller values mean bigger noise)"""
    opensimplex.seed(random.randrange(999999999))
    for x in range(map_size):
        map.append([])
        for y in range(map_size):
            if (y == 0 or y == map_size-1) or (x == 0 or x == map_size-1):
                map[x].append(1)
            else:
                noise = opensimplex.noise2(x*noise_scale, y*noise_scale)
                if noise > 0:
                    noise = 2
                else:
                    noise = 0
                map[x].append(noise)

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
        # NOTE: Because of the way python lists work, if a ray
        # goes in the negative direction, it will wrap around
        # to the end of the list. So the world will loop once.
        # pretty cool bug.
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

        if wall == 1:
            color = (color*0.3, color*0.3, color*0.3)
        elif wall == 2:
            color = (color*0.3, color*0.5, color*0.8)

        pygame.draw.line(raycast_surface, color, (x, RAYCAST_HALF_HEIGHT - wall_height), (x, RAYCAST_HALF_HEIGHT + wall_height))
        ray_angle += increment_angle

pygame.init()
raycast_surface = pygame.surface.Surface((RAYCAST_WIDTH, RAYCAST_HEIGHT))
screen = pygame.display.set_mode((1280, 960))

player = Player()

# TODO add toggleable top down view

generate_map(100, 0.2)

def render_2d(surface):
    pygame.draw.rect(surface, (50, 50, 50), pygame.Rect(0, 0, len(map), len(map)))

    for x in range(len(map)):
        for y in range(len(map)):
            if map[x][y] != 0:
                pygame.draw.line(surface, ((175, 140, 200)), (x, y), (x,y))

    pygame.draw.circle(surface, (255, 255, 255), player.pos, 2)
    ray_left = player.angle - Player.HALF_FOV
    ray_left = Vector2(
        math.cos(math.radians(ray_left)),
        math.sin(math.radians(ray_left))
    )*50
    pygame.draw.line(surface, (255, 255, 255), player.pos, player.pos+ray_left)

    ray_right = player.angle + Player.HALF_FOV
    ray_right = Vector2(
        math.cos(math.radians(ray_right)),
        math.sin(math.radians(ray_right))
    )*50
    pygame.draw.line(surface, (255, 255, 255), player.pos, player.pos+ray_right)

preview_2d_map = True

while True:
    loop_start_time = pygame.time.get_ticks()/1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                preview_2d_map = not preview_2d_map

    player.update()

    ceiling_and_floor((0.2, 0.2, 0.2), (0.3, 0.2, 0.1))
    raycast()

    screen.blit(pygame.transform.scale(raycast_surface, (screen.get_width(), screen.get_height())), (0, 0))
    
    if preview_2d_map:
        preview_surface = pygame.Surface((100, 100))
        render_2d(preview_surface)
        screen.blit(pygame.transform.scale(preview_surface, (300, 300)), (0, 0))


    pygame.display.flip()
    
    delta_time = pygame.time.get_ticks()/1000 - loop_start_time
