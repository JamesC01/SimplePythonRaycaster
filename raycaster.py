# A simple pygame raycaster started on 19/07/2022 by James Czekaj
# I enjoyed making this. I used my previous experience from the lodev tutorial, and now a more
# simple tutorial here: https://github.com/vinibiavatti1/RayCastingTutorial
# I simplified some things in that tutorial, and now I believe I finally fully understand how
# a raycaster works.

import random
import pygame, sys, math
from pygame import Vector2
import opensimplex
from player import Player
#from pygame.math import clamp # waiting for next pygame release

def clamp(val, minval, maxval):
    return min(max(minval, val), maxval)

# Size of the raycaster surface
RAYCAST_WIDTH = 320
RAYCAST_HEIGHT = 240
RAYCAST_HALF_WIDTH = int(RAYCAST_WIDTH/2)
RAYCAST_HALF_HEIGHT = int(RAYCAST_HEIGHT/2)

map = []

ray_angle_increment = Player.FOV / RAYCAST_WIDTH
ray_precision = 0.1 # ray increment amount

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

def render_floor_or_ceiling(*, which, light_color: pygame.Color, dark_color: pygame.Color):
    which = which.lower()
    if which == 'ceiling':
        draw_range = range(0, RAYCAST_HALF_HEIGHT)
        start_color = light_color
        end_color = dark_color
        offset = 0
    elif which == 'floor':
        draw_range = range(RAYCAST_HALF_HEIGHT, RAYCAST_HEIGHT)
        start_color = dark_color
        end_color = light_color
        offset = RAYCAST_HALF_HEIGHT
    else:
        raise Exception('Error: invalid option for which. Has to be \'ceiling\' or \'floor\'')

    for y in draw_range:
        color = start_color.lerp(end_color, clamp((y-offset)/draw_range.stop, 0, 1))

        pygame.draw.line(raycast_surface, tuple(color), (0, y), (RAYCAST_WIDTH, y))

    

WALL_UNBREAKABLE_COLOR = (100, 100, 100)
WALL_BREAKABLE_COLOR = (21, 100, 51)
SKY_COLOR = (107, 191, 255)
GROUND_COLOR = (71, 201, 92)

def raycast(brightness=0.6):
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
            ray_pos += ray_dir * ray_precision
            wall = map[int(ray_pos.x)][int(ray_pos.y)]

        ray_length_xy = player.pos - ray_pos
        distance = ray_length_xy.length()

        wall_height = math.floor(RAYCAST_HEIGHT / distance) * 0.5

        match wall:
            case 1:
                base_color = WALL_UNBREAKABLE_COLOR
            case 2:
                base_color = WALL_BREAKABLE_COLOR

        lit_color = tuple(n/(distance*brightness) for n in base_color)
        color = tuple(clamp(v, 0, base_color[i]) for i, v in enumerate(lit_color)) # clamp between 0 and the corrosponding base_color value

        pygame.draw.line(raycast_surface, color, (x, RAYCAST_HALF_HEIGHT - wall_height), (x, RAYCAST_HALF_HEIGHT + wall_height))
        ray_angle += ray_angle_increment

def render_minimap(surface):
    # TODO: because colour values are being doubled, colour can't exceed 255/2. Fix this
    pygame.draw.rect(surface, tuple(clamp(v*2, 0, 255) for v in WALL_BREAKABLE_COLOR), pygame.Rect(0, 0, len(map), len(map)))
    for x in range(len(map)):
        for y in range(len(map)):
            if map[x][y] != 0:
                pygame.draw.line(surface, WALL_BREAKABLE_COLOR, (x, y), (x,y))

    def draw_angle_line(ray_angle):
        pygame.draw.circle(surface, (255, 255, 255), player.pos, 2)
        ray_angle = Vector2(
            math.cos(math.radians(ray_angle)),
            math.sin(math.radians(ray_angle))
        ) * 50
        pygame.draw.line(surface, (255, 255, 255), player.pos, player.pos+ray_angle)

    draw_angle_line(player.angle - Player.HALF_FOV)
    draw_angle_line(player.angle + Player.HALF_FOV)

pygame.init()
raycast_surface = pygame.surface.Surface((RAYCAST_WIDTH, RAYCAST_HEIGHT))
screen = pygame.display.set_mode((960, 720))

player = Player()

generate_map(100, 0.2)

show_minimap = True
min
# TODO: Refactor code (make functions less coupled to global vars)
#       Make functions take color values/find a better way to deal with
#       colours. Also, just generally polish the code a bit.

delta_time = pygame.time.get_ticks()/1000

font = pygame.font.Font(None, 32)

MINIMAP_SIZE = 200

while True:
    loop_start_time = pygame.time.get_ticks()/1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                show_minimap = not show_minimap
            elif event.key == pygame.K_SPACE:
                    # Raycast directly forward and delete wall if it hits one
                    ray = player.pos.copy()
                    wall = 0
                    while wall == 0:
                        ray += player.angle_xy() * ray_precision
                        wall = map[int(ray.x)][int(ray.y)]
                    if wall == 2:
                        map[int(ray.x)][int(ray.y)] = 0

    player.update(delta_time, map)

    render_floor_or_ceiling(which='ceiling', light_color=pygame.Color(SKY_COLOR), dark_color=pygame.Color(0,0,0))
    render_floor_or_ceiling(which='floor', light_color=pygame.Color(GROUND_COLOR), dark_color=pygame.Color(0,0,0))
    raycast()

    screen.blit(pygame.transform.scale(raycast_surface, (screen.get_width(), screen.get_height())), (0, 0))
    
    if show_minimap:
        # Render minimap
        minimap_surf = pygame.Surface((100, 100))
        render_minimap(minimap_surf)
        screen.blit(pygame.transform.scale(minimap_surf, (MINIMAP_SIZE, MINIMAP_SIZE)), (0, 0))
        
        # Also render FPS
        fps_text = font.render(f'FPS: {int(1/delta_time)}', False, (255, 255, 255))
        screen.blit(fps_text, (0, MINIMAP_SIZE))

    # Render crosshair
    crosshair_surf = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
    pygame.draw.circle(crosshair_surf, pygame.Color(255, 255, 255, 70), (screen.get_width()/2, screen.get_height()/2), 5, )
    screen.blit(crosshair_surf, (0,0))
    
    pygame.display.flip()

    delta_time = pygame.time.get_ticks()/1000 - loop_start_time
