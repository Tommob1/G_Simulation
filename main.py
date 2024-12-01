import pygame
import math
import numpy as np
import sounddevice as sd

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
thrusting = False      # Declare thrusting globally

# Audio Parameters
SAMPLE_RATE = 44100
AMPLITUDE = 0.2  # Volume (0.0 to 1.0)

def generate_white_noise(duration, sample_rate=SAMPLE_RATE):
    """Generate pure white noise."""
    n_samples = int(sample_rate * duration)
    return np.random.uniform(-AMPLITUDE, AMPLITUDE, n_samples).astype(np.float32)
white_noise = generate_white_noise(1.0)

def audio_callback(outdata, frames, time, status):
    """Fills the audio output buffer with true white noise."""
    global thrusting
    if thrusting:
        # Generate random white noise for the current audio frame
        outdata[:] = np.random.uniform(-AMPLITUDE, AMPLITUDE, frames).astype(np.float32)[:, np.newaxis]
    else:
        outdata[:] = np.zeros((frames, 1))  # Silence when not thrusting
       
# Open a sounddevice output stream
stream = sd.OutputStream(
    samplerate=SAMPLE_RATE,
    channels=1,
    callback=audio_callback,
)
stream.start()

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

    # Update thrusting state globally
    thrusting = keys[pygame.K_UP]

    # Apply thrust
    if thrusting:
        acceleration = 0.2
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

stream.stop()
pygame.quit()