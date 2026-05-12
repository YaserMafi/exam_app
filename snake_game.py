"""
Snake Game - بازی مار
A classic Snake game built with Pygame.
Use arrow keys to control the snake. Eat food to grow. Don't hit the walls or yourself!
"""

import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
CELL_SIZE = 20

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 155, 0)
RED = (220, 50, 50)
GRAY = (40, 40, 40)
YELLOW = (255, 215, 0)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Game settings
FPS = 10


class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake Game - بازی مار 🐍")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 24)
        self.big_font = pygame.font.SysFont("arial", 48, bold=True)
        self.reset()

    def reset(self):
        """Reset game state for a new game."""
        center_x = SCREEN_WIDTH // (2 * CELL_SIZE)
        center_y = SCREEN_HEIGHT // (2 * CELL_SIZE)
        self.snake = [(center_x, center_y), (center_x - 1, center_y), (center_x - 2, center_y)]
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.food = None
        self.score = 0
        self.game_over = False
        self.place_food()

    def place_food(self):
        """Place food at a random position not occupied by the snake."""
        cols = SCREEN_WIDTH // CELL_SIZE
        rows = SCREEN_HEIGHT // CELL_SIZE
        while True:
            pos = (random.randint(0, cols - 1), random.randint(0, rows - 1))
            if pos not in self.snake:
                self.food = pos
                break

    def handle_events(self):
        """Handle keyboard and window events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_SPACE:
                        self.reset()
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                else:
                    if event.key == pygame.K_UP and self.direction != DOWN:
                        self.next_direction = UP
                    elif event.key == pygame.K_DOWN and self.direction != UP:
                        self.next_direction = DOWN
                    elif event.key == pygame.K_LEFT and self.direction != RIGHT:
                        self.next_direction = LEFT
                    elif event.key == pygame.K_RIGHT and self.direction != LEFT:
                        self.next_direction = RIGHT
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

    def update(self):
        """Update game state: move snake, check collisions."""
        if self.game_over:
            return

        self.direction = self.next_direction
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        # Check wall collision
        cols = SCREEN_WIDTH // CELL_SIZE
        rows = SCREEN_HEIGHT // CELL_SIZE
        if new_head[0] < 0 or new_head[0] >= cols or new_head[1] < 0 or new_head[1] >= rows:
            self.game_over = True
            return

        # Check self collision
        if new_head in self.snake:
            self.game_over = True
            return

        self.snake.insert(0, new_head)

        # Check food
        if new_head == self.food:
            self.score += 10
            self.place_food()
        else:
            self.snake.pop()

    def draw_grid(self):
        """Draw a subtle grid background."""
        for x in range(0, SCREEN_WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, GRAY, (0, y), (SCREEN_WIDTH, y))

    def draw(self):
        """Draw everything on screen."""
        self.screen.fill(BLACK)
        self.draw_grid()

        # Draw snake
        for i, (x, y) in enumerate(self.snake):
            color = GREEN if i == 0 else DARK_GREEN
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, BLACK, rect, 1)

        # Draw food
        if self.food:
            fx, fy = self.food
            food_rect = pygame.Rect(fx * CELL_SIZE, fy * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, RED, food_rect)
            pygame.draw.rect(self.screen, BLACK, food_rect, 1)

        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, YELLOW)
        self.screen.blit(score_text, (10, 5))

        # Draw game over screen
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            self.screen.blit(overlay, (0, 0))

            game_over_text = self.big_font.render("GAME OVER", True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
            self.screen.blit(game_over_text, text_rect)

            score_text = self.font.render(f"Score: {self.score}", True, WHITE)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
            self.screen.blit(score_text, score_rect)

            restart_text = self.font.render("Press SPACE to restart or ESC to quit", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
            self.screen.blit(restart_text, restart_rect)

        pygame.display.flip()

    def run(self):
        """Main game loop."""
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = SnakeGame()
    game.run()
