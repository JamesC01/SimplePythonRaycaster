import random
import pygame, sys, math
from pygame import Vector2

pygame.init()

screen_size = (640, 480)
screen_half_size = (screen_size[0]/2, screen_size[1]/2)

increment_angle = None
precision = 64

class Player:
    fov = 60
    half_fov = fov/2
    pos = Vector2(2,2)
    angle = 90

    SPEED = 0.1
    ROT_SPEED = 2

    @classmethod
    def update(cls):
        keys = pygame.key.get_pressed()

        angle_vec = Vector2(
            math.cos(math.radians(Player.angle)),
            math.sin(math.radians(Player.angle))
        ).normalize()

        if keys[pygame.K_UP]:
            dest = Player.pos + angle_vec * Player.SPEED
            if map[int(dest.y)][int(dest.x)] == 0:
                Player.pos = dest
        if keys[pygame.K_DOWN]:
            dest = Player.pos - angle_vec * Player.SPEED
            if map[int(dest.y)][int(dest.x)] == 0:
                    Player.pos = dest
        if keys[pygame.K_LEFT]:
            Player.angle -= Player.ROT_SPEED
        if keys[pygame.K_RIGHT]:
            Player.angle += Player.ROT_SPEED



screen_size = (320, 240)
screen_half_size = (screen_size[0]/2, screen_size[1]/2)

increment_angle = Player.fov / screen_size[1]
precision = 10

map = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

raycast_surface = pygame.surface.Surface(screen_size)
physical_screen = pygame.display.set_mode((640, 480))

def raycasting():
    rayAngle = Player.angle - Player.half_fov
    for x in range(0, screen_size[0]):
        ray = Player.pos.copy()

        # Ray path incrementers
        rayIncrement = Vector2(math.cos(math.radians(rayAngle)) / precision,
                         math.sin(math.radians(rayAngle)) / precision)
        
        # Wall finder
        wall = 0;
        while(wall == 0):
            ray += rayIncrement
            wall = map[math.floor(ray.y)][math.floor(ray.x)]

        # Pythagoras theorem
        distance = math.sqrt(math.pow(Player.pos.x - ray.x, 2) + math.pow(Player.pos.y - ray.y, 2))

        # Fish eye fix
        #distance = distance * math.cos(math.radians(rayAngle - Player.angle));

        # Wall height
        wallHeight = math.floor(screen_size[1] / distance)

        # Draw
        pygame.draw.line(raycast_surface, (random.randrange(255), random.randrange(255), random.randrange(255)), (x, screen_half_size[1] - wallHeight), (x, screen_half_size[1] + wallHeight))

        # Increment
        rayAngle += increment_angle

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    Player.update()

    raycast_surface.fill((0,0,0))
    raycasting()

    physical_screen.blit(pygame.transform.scale(raycast_surface, (640, 480)), (0, 0))
    
    pygame.display.flip()
