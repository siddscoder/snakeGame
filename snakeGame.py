import pygame
import random
import os

pygame.init()

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
grey = (200, 200, 200)
light_grey = (240, 240, 240)

# Screen dimensions
screen_width = 1211
screen_height = 603

# Initialize game window
gameWindow = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("SnakeGame")
pygame.display.update()

clock = pygame.time.Clock()
font = pygame.font.SysFont("arialblack", 40)

# Functions
def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])


def draw_gradient_background(screen, color1, color2):
    for i in range(screen_height):
        gradient = (
            color1[0] + (color2[0] - color1[0]) * i // screen_height,
            color1[1] + (color2[1] - color1[1]) * i // screen_height,
            color1[2] + (color2[2] - color1[2]) * i // screen_height,
        )
        pygame.draw.line(screen, gradient, (0, i), (screen_width, i))


def plot_snake(gameWindow, color, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size], border_radius=4)


def welcome():
    exit_game = False
    while not exit_game:
        draw_gradient_background(gameWindow, grey, light_grey)
        text_screen("Welcome to Snake Game", black, screen_width // 2 - 250, screen_height // 2 - 50)
        text_screen("Press SPACE BAR to Play!", red, screen_width // 2 - 240, screen_height // 2 + 20)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gameloop()

        pygame.display.update()
        clock.tick(60)


def gameloop():
    # Game variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    snake_size = 27
    velocity_x = 0
    velocity_y = 0
    init_velocity = 5
    food_x = random.randint(0, screen_width // snake_size) * snake_size
    food_y = random.randint(0, screen_height // snake_size) * snake_size
    score = 0
    fps = 32

    if not os.path.exists("highScore.txt"):
        with open("highScore.txt", "w") as f:
            f.write("0")

    try:
        with open("highScore.txt", "r") as f:
            highScore = int(f.read())
    except FileNotFoundError:
        highScore = 0

    snk_list = []
    snk_length = 1

    while not exit_game:
        if game_over:
            with open("highScore.txt", "w") as f:
                f.write(str(highScore))

            draw_gradient_background(gameWindow, grey, light_grey)
            text_screen("Game Over!", red, screen_width // 2 - 100, screen_height // 2 - 50)
            text_screen("Press ENTER to Restart", black, screen_width // 2 - 180, screen_height // 2 + 20)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        gameloop()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

            snake_x += velocity_x
            snake_y += velocity_y

            # Check for collision with food
            if abs(snake_x - food_x) < snake_size and abs(snake_y - food_y) < snake_size:
                score += 10
                food_x = random.randint(0, screen_width // snake_size) * snake_size
                food_y = random.randint(0, screen_height // snake_size) * snake_size
                snk_length += 5
                if score > highScore:
                    highScore = score

            draw_gradient_background(gameWindow, grey, light_grey)
            text_screen(f"Score: {score}  High Score: {highScore}", black, 10, 10)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size], border_radius=5)

            head = [snake_x, snake_y]
            snk_list.append(head)

            if len(snk_list) > snk_length:
                del snk_list[0]

            if head in snk_list[:-1] or snake_x < 0 or snake_x > screen_width - snake_size or snake_y < 0 or snake_y > screen_height - snake_size:
                game_over = True

            plot_snake(gameWindow, black, snk_list, snake_size)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()


welcome()
