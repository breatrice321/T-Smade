# play game
import pygame
import time
import random

def play_snake_game(game_duration=600):
    # Initialize pygame
    pygame.init()

    # Define game window dimensions
    window_x = 720
    window_y = 480

    # Define colors
    black = pygame.Color(0, 0, 0)
    white = pygame.Color(255, 255, 255)
    red = pygame.Color(255, 0, 0)
    green = pygame.Color(0, 255, 0)

    # Create game window
    game_window = pygame.display.set_mode((window_x, window_y))

    # Control frame rate with FPS
    fps = pygame.time.Clock()

    # Define initial position of the snake
    snake_position = [100, 50]

    # Define initial length of the snake
    snake_body = [[100, 50],
                  [90, 50],
                  [80, 50],
                  [70, 50]]

    # Define food position
    food_position = [random.randrange(1, (window_x // 10)) * 10,
                     random.randrange(1, (window_y // 10)) * 10]
    food_spawn = True

    # Initial score
    score = 0

    # Record game start time
    start_time = time.time()

    # Game over function
    def game_over():
        pygame.quit()
        quit()

    # Show score function
    def show_score(choice, color, font, size):
        score_font = pygame.font.SysFont(font, size)
        score_surface = score_font.render('Score : ' + str(score), True, color)
        score_rect = score_surface.get_rect()
        game_window.blit(score_surface, score_rect)

    # Automatic control logic function
    def auto_move(snake_position, food_position, snake_body):
        # Get the coordinates of the snake's head
        head_x, head_y = snake_position

        # Try to move towards the food direction
        if head_x < food_position[0]:
            new_direction = 'RIGHT'
        elif head_x > food_position[0]:
            new_direction = 'LEFT'
        elif head_y < food_position[1]:
            new_direction = 'DOWN'
        else:
            new_direction = 'UP'

        # Check if it will hit the body or walls
        if new_direction == 'RIGHT' and (head_x + 10 >= window_x or [head_x + 10, head_y] in snake_body):
            new_direction = 'UP' if head_y > 0 else 'DOWN'
        elif new_direction == 'LEFT' and (head_x - 10 < 0 or [head_x - 10, head_y] in snake_body):
            new_direction = 'UP' if head_y > 0 else 'DOWN'
        elif new_direction == 'UP' and (head_y - 10 < 0 or [head_x, head_y - 10] in snake_body):
            new_direction = 'RIGHT' if head_x < window_x else 'LEFT'
        elif new_direction == 'DOWN' and (head_y + 10 >= window_y or [head_x, head_y + 10] in snake_body):
            new_direction = 'RIGHT' if head_x < window_x else 'LEFT'

        return new_direction

    # Main game loop
    direction = 'RIGHT'

    while True:
        # Handle exit events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Automatically control the snake's direction
        direction = auto_move(snake_position, food_position, snake_body)

        # Update the snake's position based on direction
        if direction == 'UP':
            snake_position[1] -= 10
        if direction == 'DOWN':
            snake_position[1] += 10
        if direction == 'LEFT':
            snake_position[0] -= 10
        if direction == 'RIGHT':
            snake_position[0] += 10

        # Increase the snake's length
        snake_body.insert(0, list(snake_position))
        if snake_position == food_position:
            score += 10
            food_spawn = False
        else:
            snake_body.pop()

        # Generate new food
        if not food_spawn:
            food_position = [random.randrange(1, (window_x // 10)) * 10,
                             random.randrange(1, (window_y // 10)) * 10]
        food_spawn = True

        # Draw background
        game_window.fill(black)

        # Draw the snake
        for pos in snake_body:
            pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

        # Draw the food
        pygame.draw.rect(game_window, white, pygame.Rect(food_position[0], food_position[1], 10, 10))

        # Check game over conditions
        if (snake_position[0] < 0 or snake_position[0] >= window_x or
                snake_position[1] < 0 or snake_position[1] >= window_y):
            game_over()

        # Check if the snake has hit itself
        for block in snake_body[1:]:
            if snake_position == block:
                game_over()

        # Show score
        show_score(1, white, 'times new roman', 20)

        # Refresh screen
        pygame.display.update()

        # Control game speed
        fps.tick(15)

        # Calculate elapsed game time
        elapsed_time = time.time() - start_time
        if elapsed_time >= game_duration:
            print(f"Game over! You survived for {game_duration} seconds.")
            game_over()

# Main function
if __name__ == "__main__":
    play_snake_game()  # The game lasts for 600 seconds
