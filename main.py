import pygame
import math

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RCS Thruster Simulation")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

clock = pygame.time.Clock()


position = [400, 300]
velocity = [0, 0]
angle = 0
angular_velocity = 0
thrusting = False

pygame.mixer.init()
thrust_sound = pygame.mixer.Sound(pygame.mixer.Sound(pygame.examples.__path__[0] + '/data/car_door.wav'))

def rotate_point(point, angle, center):
    radians = math.radians(angle)
    x, y = point
    cx, cy = center
    x -= cx
    y -= cy
    new_x = x * math.cos(radians) - y * math.sin(radians) + cx
    new_y = x * math.sin(radians) + y * math.cos(radians) + cy
    return new_x, new_y

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        angular_velocity = -2
    elif keys[pygame.K_RIGHT]:
        angular_velocity = 2
    else:
        angular_velocity = 0

    thrusting = keys[pygame.K_UP]

    if thrusting:
        pygame.mixer.Sound.play(thrust_sound)
        acceleration = 0.2
        velocity[0] += acceleration * math.sin(math.radians(angle))
        velocity[1] -= acceleration * math.cos(math.radians(angle))

    position[0] += velocity[0]
    position[1] += velocity[1]
    angle += angular_velocity

    position[0] %= WIDTH
    position[1] %= HEIGHT

    screen.fill(BLACK)

    center = (position[0], position[1])
    points = [
        rotate_point((position[0], position[1] - 15), angle, center),
        rotate_point((position[0] - 10, position[1] + 10), angle, center),
        rotate_point((position[0] + 10, position[1] + 10), angle, center),
    ]
    pygame.draw.polygon(screen, WHITE, points)

    if thrusting:
        flame_points = [
            rotate_point((position[0] - 5, position[1] + 12), angle, center),
            rotate_point((position[0] + 5, position[1] + 12), angle, center),
            rotate_point((position[0], position[1] + 25), angle, center),
        ]
        pygame.draw.polygon(screen, RED, flame_points)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()