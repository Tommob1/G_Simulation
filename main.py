import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RCS Thruster Simulation")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

clock = pygame.time.Clock()

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