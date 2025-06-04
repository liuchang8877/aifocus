import pygame
import random
import math
import array

# Screen dimensions
WIDTH, HEIGHT = 640, 480
CELL_SIZE = 20

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Initialize pygame
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=1)

def generate_beep(frequency=880, duration_ms=150, volume=0.5):
    sample_rate = 44100
    n_samples = int(sample_rate * duration_ms / 1000)
    buf = array.array('h')
    for s in range(n_samples):
        t = s / sample_rate
        amplitude = int(volume * 32767 * math.sin(2 * math.pi * frequency * t))
        buf.append(amplitude)
    return pygame.mixer.Sound(buffer=buf.tobytes())

eat_sound = generate_beep()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()


def draw_rect(color, position):
    rect = pygame.Rect(position[0], position[1], CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, color, rect)


def random_position():
    x = random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
    y = random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
    return x, y


def main():
    snake = [(WIDTH // 2, HEIGHT // 2)]
    direction = (CELL_SIZE, 0)
    food = random_position()
    running = True
    anim_color = 0

    while running:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, CELL_SIZE):
                    direction = (0, -CELL_SIZE)
                elif event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                    direction = (0, CELL_SIZE)
                elif event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                    direction = (-CELL_SIZE, 0)
                elif event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                    direction = (CELL_SIZE, 0)

        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        if (
            new_head[0] < 0 or new_head[0] >= WIDTH or
            new_head[1] < 0 or new_head[1] >= HEIGHT or
            new_head in snake
        ):
            running = False
            continue

        snake.insert(0, new_head)
        if new_head == food:
            if eat_sound:
                eat_sound.play()
            food = random_position()
        else:
            snake.pop()

        screen.fill(BLACK)
        anim_color = (anim_color + 5) % 255
        color = (anim_color, 255 - anim_color, 128)
        for segment in snake:
            draw_rect(color, segment)
        draw_rect(RED, food)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
