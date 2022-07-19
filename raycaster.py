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
    x = 2
    y = 2
    angle = 90

screen_size = (640, 480)
screen_half_size = (screen_size[0]/2, screen_size[1]/2)

increment_angle = Player.fov / screen_size[1]
precision = 64

map = [
    [1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,0,0,1,1,0,1,0,0,1],
    [1,0,0,1,0,0,1,0,0,1],
    [1,0,0,1,0,0,1,0,0,1],
    [1,0,0,1,0,1,1,0,0,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1]
]

screen = pygame.display.set_mode(screen_size)

def raycasting():
    rayAngle = Player.angle - Player.half_fov
    for x in range(0, screen_size[0]):
        ray = Vector2(Player.x, Player.y)

        # Ray path incrementers
        rayIncrement = Vector2(math.cos(math.radians(rayAngle)) / precision,
                         math.sin(math.radians(rayAngle)) / precision)
        
        # Wall finder
        wall = 0;
        while(wall == 0):
            ray += rayIncrement
            wall = map[math.floor(ray.y)][math.floor(ray.x)]

        # Pythagoras theorem
        distance = math.sqrt(math.pow(Player.x - ray.x, 2) + math.pow(Player.y - ray.y, 2))

        # Fish eye fix
        #distance = distance * Math.cos(degreeToRadians(rayAngle - data.player.angle));

        # Wall height
        wallHeight = math.floor(screen_size[1] / distance)

        # Draw
        pygame.draw.line(screen, (5, 100, 100), (x, screen_half_size[1] - wallHeight), (x, screen_half_size[1] + wallHeight))

        # Increment
        rayAngle += increment_angle

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill((0,0,0))

    raycasting()

    
    pygame.display.flip()
