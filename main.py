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

    screen.fill(BLACK)
    pygame.draw.polygon(screen, WHITE, [(400, 300), (390, 320), (410, 320)])
    pygame.display.flip()
    clock.tick(60)

pygame.quit()