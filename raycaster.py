# A simple pygame raycaster started on 19/07/2022 by James Czekaj
# I enjoyed making this. I used my previous experience from the lodev tutorial, and now a more
# simple tutorial here: https://github.com/vinibiavatti1/RayCastingTutorial
# I simplified some things in that tutorial, and now I believe I finally fully understand how
# a raycaster works.

import random, sys, math
import opensimplex
import pygame as pg
from pygame import Vector2
from player import Player
#from pygame.math import clamp # waiting for next pygame release

def clamp(val, minval, maxval):
    return min(max(minval, val), maxval)

# Colour constants
WALL_UNBREAKABLE_COLOR = (100, 100, 100)
WALL_BREAKABLE_COLORS = []
for i in range(1000):
    WALL_BREAKABLE_COLORS.append((random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)))

SKY_COLOR = (107, 191, 255)
GROUND_COLOR = (71, 201, 92)

# Size of the raycaster surface
RAYCAST_WIDTH = 320
RAYCAST_HEIGHT = 240
RAYCAST_HALF_WIDTH = int(RAYCAST_WIDTH/2)
RAYCAST_HALF_HEIGHT = int(RAYCAST_HEIGHT/2)

MINIMAP_SIZE = 200

# 0 = empty, 1 = unbreakable, >1 = breakable
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
                    # Select colour based
                    grid_val = 2
                    step = 1 / len(WALL_BREAKABLE_COLORS)
                    current = 0
                    for i in range(len(WALL_BREAKABLE_COLORS)):
                        if noise > (current := current + step):
                            grid_val = 3+i
                else:
                    grid_val = 0
                map[x].append(grid_val)

def render_floor_or_ceiling(*, which, light_color: pg.Color, dark_color: pg.Color):
    """Renders the floor or ceiling

        Arguments:
        which -- Either 'ceiling' or 'floor'
        light_color -- the lightest color of the ceiling or floor
        dark_color -- the darkest color of the ceiling or floor"""

    which = which.lower()
    if which == 'ceiling':
        draw_range = range(0, RAYCAST_HALF_HEIGHT)
        start_color = light_color
        end_color = dark_color
        yoffset = 0
    elif which == 'floor':
        draw_range = range(RAYCAST_HALF_HEIGHT, RAYCAST_HEIGHT)
        start_color = dark_color
        end_color = light_color
        yoffset = RAYCAST_HALF_HEIGHT
    else:
        raise Exception('Error: invalid option for which. Has to be \'ceiling\' or \'floor\'')

    for y in draw_range:
        color = start_color.lerp(end_color, clamp((y-yoffset)/draw_range.stop, 0, 1))

        pg.draw.line(raycast_surface, tuple(color), (0, y), (RAYCAST_WIDTH, y))


def raycast(brightness=0.6):
    """Raycast rendering

        Arguments:
        brightness -- the intensity of the lighting (smaller values make light brighter.)"""
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

        # solve fisheye effect (rays near to edge of fov need to go further, so
        # you scale them by cos(rayangle/playerangle) to scale them to the same
        # length that they would be, had they been cast from the playerangle.
        distance *= math.cos(math.radians(ray_angle)-math.radians(player.angle))


        wall_height = math.floor(RAYCAST_HEIGHT / distance) * 0.5

        if wall == 1:
            base_color = WALL_UNBREAKABLE_COLOR
        elif wall >= 2:
            base_color = WALL_BREAKABLE_COLORS[wall-2]
        else:
            base_color = (1,1,1)

        lit_color = tuple(n/(distance*brightness) for n in base_color)
        color = tuple(clamp(v, 0, base_color[i]) for i, v in enumerate(lit_color)) # clamp between 0 and the corrosponding base_color value

        pg.draw.line(raycast_surface, color, (x, RAYCAST_HALF_HEIGHT - wall_height), (x, RAYCAST_HALF_HEIGHT + wall_height))
        ray_angle += ray_angle_increment

def render_minimap(surface):
    # TODO: because colour values are being doubled, colour can't exceed 255/2. Fix this
    pg.draw.rect(surface, tuple(clamp(v*2, 0, 255) for v in WALL_BREAKABLE_COLORS[0]), pg.Rect(0, 0, len(map), len(map)))
    for x in range(len(map)):
        for y in range(len(map)):
            if map[x][y] != 0:
                pg.draw.line(surface, WALL_BREAKABLE_COLORS[0], (x, y), (x,y))

    def draw_angle_line(ray_angle):
        pg.draw.circle(surface, (255, 255, 255), player.pos, 2)
        ray_angle = Vector2(
            math.cos(math.radians(ray_angle)),
            math.sin(math.radians(ray_angle))
        ) * 50
        pg.draw.line(surface, (255, 255, 255), player.pos, player.pos+ray_angle)

    draw_angle_line(player.angle - Player.HALF_FOV)
    draw_angle_line(player.angle + Player.HALF_FOV)

def break_wall():
    """Casts a ray forward from the player until it hits a wall. Breaks the wall if it's breakable."""
    ray = player.pos.copy()
    wall = 0
    while wall == 0:
        ray += player.angle_xy() * ray_precision
        wall = map[int(ray.x)][int(ray.y)]
    if wall > 1:
        map[int(ray.x)][int(ray.y)] = 0

def render():
    render_floor_or_ceiling(which='ceiling', light_color=pg.Color(SKY_COLOR), dark_color=pg.Color(0,0,0))
    render_floor_or_ceiling(which='floor', light_color=pg.Color(GROUND_COLOR), dark_color=pg.Color(0,0,0))
    raycast()

    screen.blit(pg.transform.scale(raycast_surface, (screen.get_width(), screen.get_height())), (0, 0))

    if show_minimap:
        # Render minimap
        minimap_surf = pg.Surface((100, 100))
        render_minimap(minimap_surf)
        screen.blit(pg.transform.scale(minimap_surf, (MINIMAP_SIZE, MINIMAP_SIZE)), (0, 0))

        # Also render FPS
        fps_text = font.render(f'FPS: {int(1/delta_time)}', False, (255, 255, 255))
        screen.blit(fps_text, (0, MINIMAP_SIZE))

    # Render crosshair
    crosshair_surf = pg.Surface((screen.get_width(), screen.get_height()), pg.SRCALPHA)
    pg.draw.circle(crosshair_surf, pg.Color(255, 255, 255, 70), (screen.get_width()/2, screen.get_height()/2), 5, )
    screen.blit(crosshair_surf, (0,0))

# TODO: Refactor code (make functions less coupled to global vars)
#       Make functions take color values/find a better way to deal with
#       colours. Also, just generally polish the code a bit.
#       Enable a max raycast distance to save performance (try to make it look
#       nicer than walls just popping in)

# Initialization
pg.init()
raycast_surface = pg.surface.Surface((RAYCAST_WIDTH, RAYCAST_HEIGHT))
screen = pg.display.set_mode((960, 720))

player = Player()
generate_map(100, 0.2)
show_minimap = True

delta_time = 1/60

font = pg.font.Font(None, 32)

# Main loop
while True:
    loop_start_time = pg.time.get_ticks()/1000

    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_m:
                show_minimap = not show_minimap
            elif event.key == pg.K_SPACE:
                    break_wall()

    player.update(delta_time, map)

    render()
    pg.display.flip()

    delta_time = pg.time.get_ticks()/1000 - loop_start_time
