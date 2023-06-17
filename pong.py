import pygame
import random

#Initialize Pygame
pygame.init()

#window
window_width = 800
window_height = 400
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Pong Game")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#paddles
paddle_width = 10
paddle_height = 60
paddle_speed = 5
paddle1_pos = window_height // 2 - paddle_height // 2
paddle2_pos = window_height // 2 - paddle_height // 2

#ball
ball_radius = 10
ball_pos = [window_width // 2, window_height // 2]
ball_speed_x = random.choice([-1, 1]) * random.randint(2, 4)
ball_speed_y = random.choice([-1, 1]) * random.randint(2, 4)
ball_size = ball_radius
ball_max_size = 30
ball_min_size = 10

#rgb
paddle_rgb_r = random.randint(0, 255)
paddle_rgb_g = random.randint(0, 255)
paddle_rgb_b = random.randint(0, 255)
paddle_rgb_change_speed = 1

ball_rgb_r = random.randint(0, 255)
ball_rgb_g = random.randint(0, 255)
ball_rgb_b = random.randint(0, 255)
ball_rgb_change_speed = 1

# players names
player1_name = input("Enter Player 1's Name: ")
player2_name = input("Enter Player 2's Name: ")

# game type
game_type = input("Choose game type: [T]imer or [S]core Limit: ").lower()
if game_type == "t":
    game_duration = int(input("Enter game duration in seconds: "))
    score_limit = None
elif game_type == "s":
    score_limit = int(input("Enter score limit: "))
    game_duration = None
else:
    print("Invalid input. Defaulting to timer with 50 seconds.")
    game_duration = 50
    score_limit = None

# game difficulty
difficulty = int(input("Choose game difficulty (1-5): "))
ball_speed_x *= difficulty
ball_speed_y *= difficulty

# scores
score1 = 0
score2 = 0

#game clock
clock = pygame.time.Clock()
running = True

start_ticks = pygame.time.get_ticks()

while running:
    # check game end
    if game_duration is not None:
        seconds = (pygame.time.get_ticks() - start_ticks) // 1000
        if seconds >= game_duration:
            if score1 > score2:
                winner = player1_name
            elif score2 > score1:
                winner = player2_name
            else:
                winner = "Draw"
            print("Game Over! {} won.".format(winner))
            running = False
    elif score_limit is not None:
        if score1 >= score_limit or score2 >= score_limit:
            if score1 > score2:
                winner = player1_name
            elif score2 > score1:
                winner = player2_name
            else:
                winner = "Draw"
            print("Game Over! {} won.".format(winner))
            running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and paddle1_pos > 0:
        paddle1_pos -= paddle_speed
    if keys[pygame.K_s] and paddle1_pos < window_height - paddle_height:
        paddle1_pos += paddle_speed
    if keys[pygame.K_UP] and paddle2_pos > 0:
        paddle2_pos -= paddle_speed
    if keys[pygame.K_DOWN] and paddle2_pos < window_height - paddle_height:
        paddle2_pos += paddle_speed

    ball_pos[0] += ball_speed_x
    ball_pos[1] += ball_speed_y

    # collision
    if ball_pos[1] <= 0 or ball_pos[1] >= window_height - ball_radius:
        ball_speed_y *= -1
    if ball_pos[0] <= paddle_width and paddle1_pos <= ball_pos[1] <= paddle1_pos + paddle_height:
        ball_speed_x *= -1
        ball_size = random.randint(ball_min_size, ball_max_size)
    if ball_pos[0] >= window_width - paddle_width - ball_radius and paddle2_pos <= ball_pos[1] <= paddle2_pos + paddle_height:
        ball_speed_x *= -1
        ball_size = random.randint(ball_min_size, ball_max_size)

    # checking
    if ball_pos[0] <= 0:
        score2 += 1
        ball_pos = [window_width // 2, window_height // 2]
        ball_speed_x *= -1
        ball_size = ball_radius
    if ball_pos[0] >= window_width - ball_radius:
        score1 += 1
        ball_pos = [window_width // 2, window_height // 2]
        ball_speed_x *= -1
        ball_size = ball_radius

    # RGB aesthetics
    if paddle_rgb_r >= 255 or paddle_rgb_r <= 0:
        paddle_rgb_change_speed *= -1
    paddle_rgb_r += paddle_rgb_change_speed
    paddle_rgb_g = (paddle_rgb_g + paddle_rgb_change_speed) % 255
    paddle_rgb_b = (paddle_rgb_b + paddle_rgb_change_speed) % 255

    if ball_rgb_r >= 255 or ball_rgb_r <= 0:
        ball_rgb_change_speed *= -1
    ball_rgb_r += ball_rgb_change_speed
    ball_rgb_g = (ball_rgb_g + ball_rgb_change_speed) % 255
    ball_rgb_b = (ball_rgb_b + ball_rgb_change_speed) % 255


    window.fill(BLACK)

    # paddles
    pygame.draw.rect(window, (paddle_rgb_r, paddle_rgb_g, paddle_rgb_b), (0, paddle1_pos, paddle_width, paddle_height))
    pygame.draw.rect(window, (paddle_rgb_r, paddle_rgb_g, paddle_rgb_b), (window_width - paddle_width, paddle2_pos, paddle_width, paddle_height))

    # ball
    pygame.draw.circle(window, (ball_rgb_r, ball_rgb_g, ball_rgb_b), (int(ball_pos[0]), int(ball_pos[1])), ball_size)

    # players' names and scores
    font = pygame.font.Font(None, 30)
    player1_text = font.render("{}: {}".format(player1_name, score1), True, WHITE)
    player2_text = font.render("{}: {}".format(player2_name, score2), True, WHITE)
    window.blit(player1_text, (10, 10))
    window.blit(player2_text, (window_width - player2_text.get_width() - 10, 10))

    pygame.display.flip()

    clock.tick(60)

# Quit the game
pygame.quit()
