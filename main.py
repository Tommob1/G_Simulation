import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RCS Thruster Simulation")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

clock = pygame.time.Clock()

position = [400, 300]
velocity = [0, 0]
angle = 0
angular_velocity = 0

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

    if keys[pygame.K_UP]:
        thrust = 0.2
        velocity[0] += thrust * math.cos(math.radians(angle))
        velocity[1] -= thrust * math.sin(math.radians(angle))
    else:
        thrust = 0

    position[0] += velocity[0]
    position[1] += velocity[1]
    angle += angular_velocity

    position[0] %= WIDTH
    position[1] %= HEIGHT

    screen.fill(BLACK)

    center = (position[0], position[1])
    points = [
        rotate_point((position[0], position[1] - 15), angle, center),  # Front
        rotate_point((position[0] - 10, position[1] + 10), angle, center),  # Left
        rotate_point((position[0] + 10, position[1] + 10), angle, center),  # Right
    ]
    pygame.draw.polygon(screen, WHITE, points)

    # Visualize thrust
    if thrust > 0:
        thrust_points = [
            rotate_point((position[0] - 5, position[1] + 15), angle, center),  # Left flame
            rotate_point((position[0] + 5, position[1] + 15), angle, center),  # Right flame
            rotate_point((position[0], position[1] + 25), angle, center),      # Tip of flame
        ]
        pygame.draw.polygon(screen, (255, 0, 0), thrust_points)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()