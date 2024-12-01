import pygame
import math

# Initialize Pygame
pygame.init()

# Screen Dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RCS Thruster Simulation")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Spacecraft properties
position = [400, 300]  # x, y
velocity = [0, 0]      # vx, vy
angle = 0              # Orientation in degrees (0 points up)
angular_velocity = 0   # Rotation speed
thrusting = False      # Is the ship thrusting?

def rotate_point(point, angle, center):
    """Rotates a point around a center by a given angle."""
    radians = math.radians(angle)
    x, y = point
    cx, cy = center
    x -= cx
    y -= cy
    new_x = x * math.cos(radians) - y * math.sin(radians) + cx
    new_y = x * math.sin(radians) + y * math.cos(radians) + cy
    return new_x, new_y

# Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        angular_velocity = -2  # Rotate counterclockwise
    elif keys[pygame.K_RIGHT]:
        angular_velocity = 2  # Rotate clockwise
    else:
        angular_velocity = 0

    thrusting = keys[pygame.K_UP]  # Thrust when UP is pressed

    # Apply thrust
    if thrusting:
        acceleration = 0.2
        # Adjust thrust direction based on the ship's angle
        velocity[0] += acceleration * math.sin(math.radians(angle))
        velocity[1] -= acceleration * math.cos(math.radians(angle))

    # Update physics
    position[0] += velocity[0]
    position[1] += velocity[1]
    angle += angular_velocity

    # Screen wrap-around
    position[0] %= WIDTH
    position[1] %= HEIGHT

    # Clear the screen
    screen.fill(BLACK)

    # Draw the spacecraft
    center = (position[0], position[1])
    points = [
        rotate_point((position[0], position[1] - 15), angle, center),  # Front
        rotate_point((position[0] - 10, position[1] + 10), angle, center),  # Left
        rotate_point((position[0] + 10, position[1] + 10), angle, center),  # Right
    ]
    pygame.draw.polygon(screen, WHITE, points)

    # Draw thrust flame (on the back of the ship)
    if thrusting:
        flame_points = [
            rotate_point((position[0] - 5, position[1] + 12), angle, center),
            rotate_point((position[0] + 5, position[1] + 12), angle, center),
            rotate_point((position[0], position[1] + 25), angle, center),
        ]
        pygame.draw.polygon(screen, RED, flame_points)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()