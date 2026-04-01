import pygame, random, sys
pygame.init()
pygame.mixer.init()  # Sound system

# Game constants
SIZE = 20
WIDTH = 400
HEIGHT = 400

# Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game 🐍")
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
WHITE = (255, 255, 255)

# Font
font = pygame.font.SysFont("Arial", 24)
big_font = pygame.font.SysFont("Arial", 36)

# 🎵 Load Sounds
pygame.mixer.music.load("background.mp3")   # background music
eat_sound = pygame.mixer.Sound("eat.wav")   # food sound
gameover_sound = pygame.mixer.Sound("gameover.wav")  # game over sound

# Set volumes (0.0 = mute, 1.0 = max)
pygame.mixer.music.set_volume(0.3)   # softer background
eat_sound.set_volume(0.7)            # louder chomp
gameover_sound.set_volume(0.9)       # strong game over

# Start background music (loop forever)
pygame.mixer.music.play(-1)


def random_food(snake):
    """Generate food at a random grid position not occupied by the snake."""
    while True:
        food = (random.randrange(0, WIDTH, SIZE), random.randrange(0, HEIGHT, SIZE))
        if food not in snake:
            return food


def draw_snake(snake):
    for x, y in snake:
        pygame.draw.rect(screen, GREEN, (x, y, SIZE-1, SIZE-1))


def draw_food(food):
    pygame.draw.rect(screen, RED, (food[0], food[1], SIZE-1, SIZE-1))


def show_score(score):
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))


def game_over_screen(score):
    # Stop music and play game over sound
    pygame.mixer.music.stop()
    gameover_sound.play()

    screen.fill(BLACK)
    text = big_font.render("GAME OVER!", True, RED)
    score_text = font.render(f"Your Score: {score}", True, WHITE)
    restart_text = font.render("Press R to Restart or Q to Quit", True, WHITE)

    screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//3))
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
    screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//1.5))
    pygame.display.flip()

    # Wait for user input
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r:  # restart
                    pygame.mixer.music.play(-1)  # restart background music
                    return True
                elif e.key == pygame.K_q:  # quit
                    pygame.quit()
                    sys.exit()


def main():
    # Snake setup
    snake = [(100, 100)]
    dx, dy = SIZE, 0  # moving right by default
    food = random_food(snake)

    while True:
        # Event handling
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP and dy == 0:
                    dx, dy = 0, -SIZE
                if e.key == pygame.K_DOWN and dy == 0:
                    dx, dy = 0, SIZE
                if e.key == pygame.K_LEFT and dx == 0:
                    dx, dy = -SIZE, 0
                if e.key == pygame.K_RIGHT and dx == 0:
                    dx, dy = SIZE, 0

        # Move Snake
        head = (snake[0][0] + dx, snake[0][1] + dy)
        snake.insert(0, head)

        # Check food
        if head == food:
            eat_sound.play()  # Play eat sound
            food = random_food(snake)
        else:
            snake.pop()

        # Collision check
        if (head in snake[1:] or not 0 <= head[0] < WIDTH or not 0 <= head[1] < HEIGHT):
            if game_over_screen(len(snake)-1):
                return main()  # restart game

        # Draw everything
        screen.fill(BLACK)
        draw_snake(snake)
        draw_food(food)
        show_score(len(snake) - 1)

        pygame.display.flip()
        clock.tick(10 + len(snake)//5)  # speed increases as score grows


if __name__ == "__main__":
    main()
