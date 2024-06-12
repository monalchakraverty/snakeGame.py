from flask import Flask, render_template

import pygame
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game')
def game():
    return render_template('game.html')

if __name__ == '__main__':
    pygame.init()

    display_info = pygame.display.Info()
    WINDOW_WIDTH = display_info.current_w
    WINDOW_HEIGHT = display_info.current_h

    WINDOW_WIDTH = 1400
    WINDOW_HEIGHT = 800
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Snake Game')

    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)

    cell_size = 20
    snake_speed = 10
    snake_x = WINDOW_WIDTH // 2
    snake_y = WINDOW_HEIGHT // 2
    snake_dx = cell_size
    snake_dy = 0
    snake_length = 1
    snake_body = [(snake_x, snake_y)]
    food_x = random.randint(0, WINDOW_WIDTH - cell_size) // cell_size * cell_size
    food_y = random.randint(0, WINDOW_HEIGHT - cell_size) // cell_size * cell_size
    score = 0

    font = pygame.font.SysFont(None, 30)

    try:
        with open("high_score.txt", "r") as file:
            high_score = int(file.read())
    except FileNotFoundError:
        high_score = 0

    running = True
    clock = pygame.time.Clock()
    while running:
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_dy == 0:
                    snake_dx = 0
                    snake_dy = -cell_size
                elif event.key == pygame.K_DOWN and snake_dy == 0:
                    snake_dx = 0
                    snake_dy = cell_size
                elif event.key == pygame.K_LEFT and snake_dx == 0:
                    snake_dx = -cell_size
                    snake_dy = 0
                elif event.key == pygame.K_RIGHT and snake_dx == 0:
                    snake_dx = cell_size
                    snake_dy = 0

        snake_x += snake_dx
        snake_y += snake_dy

        if snake_x < 0 or snake_x >= WINDOW_WIDTH or snake_y < 0 or snake_y >= WINDOW_HEIGHT:
            running = False

        if snake_x == food_x and snake_y == food_y:
            snake_length += 1
            score += 10
            food_x = random.randint(0, WINDOW_WIDTH - cell_size) // cell_size * cell_size
            food_y = random.randint(0, WINDOW_HEIGHT - cell_size) // cell_size * cell_size

            if score > high_score:
                high_score = score

        snake_body.append((snake_x, snake_y))
        if len(snake_body) > snake_length:
            del snake_body[0]

        if (snake_x, snake_y) in snake_body[:-1]:
            running = False

        window.fill(WHITE)

        for body_part in snake_body:
            pygame.draw.rect(window, GREEN, (body_part[0], body_part[1], cell_size, cell_size))

        pygame.draw.rect(window, RED, (food_x, food_y, cell_size, cell_size))

        score_text = font.render("Score: " + str(score), True, (0, 0, 0))
        high_score_text = font.render("High Score: " + str(high_score), True, (0, 0, 0))
        window.blit(score_text, (10, 10))
        window.blit(high_score_text, (10, 40))

        pygame.display.flip()

        clock.tick(snake_speed)

    with open("high_score.txt", "w") as file:
        file.write(str(high_score))

    pygame.quit()
