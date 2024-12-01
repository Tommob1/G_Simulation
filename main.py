import pygame
import math
import numpy as np
import sounddevice as sd

pygame.init()
pygame.font.init()
font = pygame.font.Font(None, 20)

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

SAMPLE_RATE = 44100
AMPLITUDE = 0.2

def generate_white_noise(duration, sample_rate=SAMPLE_RATE):
    n_samples = int(sample_rate * duration)
    return np.random.uniform(-AMPLITUDE, AMPLITUDE, n_samples).astype(np.float32)
white_noise = generate_white_noise(1.0)

def low_pass_filter(noise, cutoff, sample_rate, roll_off=0.1):
    hann_window = np.hanning(len(noise))
    noise = noise * hann_window

    fft_noise = np.fft.rfft(noise)
    frequencies = np.fft.rfftfreq(len(noise), 1 / sample_rate)

    transition_band = (frequencies > cutoff) & (frequencies < cutoff * (1 + roll_off))
    fft_noise[frequencies > cutoff * (1 + roll_off)] = 0
    fft_noise[transition_band] *= np.linspace(1, 0, np.sum(transition_band))

    return np.fft.irfft(fft_noise)

def audio_callback(outdata, frames, time, status):
    global thrusting
    if thrusting:
        raw_noise = np.random.uniform(-AMPLITUDE, AMPLITUDE, frames).astype(np.float32)
        filtered_noise = low_pass_filter(raw_noise, cutoff=1000, sample_rate=SAMPLE_RATE)
        if len(filtered_noise) < frames:
            filtered_noise = np.pad(filtered_noise, (0, frames - len(filtered_noise)))
        elif len(filtered_noise) > frames:
            filtered_noise = filtered_noise[:frames]
        outdata[:] = filtered_noise[:, np.newaxis]
    else:
        outdata[:] = np.zeros((frames, 1))

stream = sd.OutputStream(
    samplerate=SAMPLE_RATE,
    channels=1,
    callback=audio_callback,
)
stream.start()

def rotate_point(point, angle, center):
    radians = math.radians(angle)
    x, y = point
    cx, cy = center
    x -= cx
    y -= cy
    new_x = x * math.cos(radians) - y * math.sin(radians) + cx
    new_y = x * math.sin(radians) + y * math.cos(radians) + cy
    return new_x, new_y

earth_mode = False
gravity = 9.8 / 60 

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                earth_mode = not earth_mode

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        angular_velocity = -2
    elif keys[pygame.K_RIGHT]:
        angular_velocity = 2
    else:
        angular_velocity = 0

    thrusting = keys[pygame.K_UP]

    if thrusting:
        acceleration = 0.2
        velocity[0] += acceleration * math.sin(math.radians(angle))
        velocity[1] -= acceleration * math.cos(math.radians(angle))

    if earth_mode:
        velocity[1] += gravity

    position[0] += velocity[0]
    position[1] += velocity[1]
    angle += angular_velocity

    position[0] %= WIDTH
    if earth_mode and position[1] > HEIGHT:
        position[1] = HEIGHT
        velocity[1] = 0
    else:
        position[1] %= HEIGHT

    if earth_mode:
        screen.fill((135, 206, 235))
    else:
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

    text = font.render("Press E to toggle Earth mode", True, WHITE)
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

stream.stop()
pygame.quit()