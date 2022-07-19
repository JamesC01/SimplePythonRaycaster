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

# Size of the raycaster surface
RAYCAST_WIDTH = 640
RAYCAST_HEIGHT = 480
RAYCAST_HALF_WIDTH = int(RAYCAST_WIDTH/2)
RAYCAST_HALF_HEIGHT = int(RAYCAST_HEIGHT/2)

class Player:
    FOV = 70
    HALF_FOV = FOV/2
    SPEED = 4
    ROTATE_SPEED = 180

    def __init__(self, pos=Vector2(2,2), angle=45):
        self.pos = pos
        self.angle = angle

    def angle_xy(self):
        """Returns the players current angle degrees as a normalized Vector2"""
        return Vector2(
            math.cos(math.radians(self.angle)),
            math.sin(math.radians(self.angle))
        ).normalize()

    def update(self, delta):
        keys = pygame.key.get_pressed()

        # Move
        if keys[pygame.K_UP]:
            dest = self.pos + self.angle_xy() * Player.SPEED * delta
            if map[int(dest.x)][int(dest.y)] == 0:
                self.pos = dest
        if keys[pygame.K_DOWN]:
            dest = self.pos - self.angle_xy() * Player.SPEED * delta
            if map[int(dest.x)][int(dest.y)] == 0:
                    self.pos = dest

        if keys[pygame.K_LALT] or keys[pygame.K_RALT]:
            right = -Vector2(self.angle_xy(), -self.angle_xy())
            # Strafe
            if keys[pygame.K_LEFT]:
                self.pos -= right * Player.SPEED * delta
            if keys[pygame.K_RIGHT]:
                self.pos += right * Player.SPEED * delta
        else:
             # Rotate
            if keys[pygame.K_LEFT]:
                self.angle -= Player.ROTATE_SPEED * delta
            if keys[pygame.K_RIGHT]:
                self.angle += Player.ROTATE_SPEED * delta

        # Reposition (not working)
        if keys[pygame.K_r]:
            self.reposition()


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

def render_floor_or_ceiling(*, which, color):
    which = which.lower()
    if which == 'ceiling':
        draw_range = range(0, RAYCAST_HALF_HEIGHT)
    elif which == 'floor':
        draw_range = range(RAYCAST_HALF_HEIGHT, RAYCAST_HEIGHT)
    else:
        raise Exception('Error: invalid option for which. Has to be \'ceiling\' or \'floor\'')

    for y in draw_range:
        new_color = list(color)
        for i in range(3):
            if which.lower() == 'floor':
                new_color[i] = new_color[i]*((y-RAYCAST_HALF_HEIGHT)/RAYCAST_HALF_HEIGHT)
            elif which.lower() == 'ceiling':
                new_color[i] = new_color[i]-(new_color[i]*(y/RAYCAST_HALF_HEIGHT))

        pygame.draw.line(raycast_surface, tuple(new_color), (0, y), (RAYCAST_WIDTH, y))

    

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
        color = tuple(min(base_color[i], max(0, v)) for i, v in enumerate(lit_color)) # clamp between 0 and the corrosponding base_color value

        pygame.draw.line(raycast_surface, color, (x, RAYCAST_HALF_HEIGHT - wall_height), (x, RAYCAST_HALF_HEIGHT + wall_height))
        ray_angle += ray_angle_increment

def render_minimap(surface):
    # TODO: because colour values are being doubled, colour can't exceed 255/2. Fix this
    pygame.draw.rect(surface, tuple(n*2 for n in WALL_BREAKABLE_COLOR), pygame.Rect(0, 0, len(map), len(map)))


    for x in range(len(map)):
        for y in range(len(map)):
            if map[x][y] != 0:
                pygame.draw.line(surface, WALL_BREAKABLE_COLOR, (x, y), (x,y))

    pygame.draw.circle(surface, (255, 255, 255), player.pos, 2)
    ray_left = player.angle - Player.HALF_FOV
    ray_left = Vector2(
        math.cos(math.radians(ray_left)),
        math.sin(math.radians(ray_left))
    ) * 50
    pygame.draw.line(surface, (255, 255, 255), player.pos, player.pos+ray_left)

    ray_right = player.angle + Player.HALF_FOV
    ray_right = Vector2(
        math.cos(math.radians(ray_right)),
        math.sin(math.radians(ray_right))
    ) * 50
    pygame.draw.line(surface, (255, 255, 255), player.pos, player.pos+ray_right)

pygame.init()
raycast_surface = pygame.surface.Surface((RAYCAST_WIDTH, RAYCAST_HEIGHT))
screen = pygame.display.set_mode((1280, 960))

player = Player()

generate_map(100, 0.2)

show_minimap = True

# TODO: Refactor code (make functions less coupled to global vars)
#       Make functions take color values/find a better way to deal with
#       colours. Also, just generally polish the code a bit.

delta_time = pygame.time.get_ticks()/1000

font = pygame.font.Font(None, 32)

MINIMAP_SIZE = 300

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

    player.update(delta_time)

    render_floor_or_ceiling(which='ceiling', color=SKY_COLOR)
    render_floor_or_ceiling(which='floor', color=GROUND_COLOR)
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
    print('FPS:', int(1/delta_time))
