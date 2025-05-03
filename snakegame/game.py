#!/usr/bin/env python3
"""
Snake Game implemented using Pygame
"""

import pygame
import sys
import random
import time
from enum import Enum, auto
from typing import List, Tuple, Optional

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

# Game settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE
FPS = 10


class Direction(Enum):
    """Enum for snake direction"""
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


class Snake:
    """Snake class representing the player"""
    
    def __init__(self):
        """Initialize the snake in the middle of the screen"""
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        self.grow_pending = False
        
    def get_head_position(self) -> Tuple[int, int]:
        """Get the position of the snake's head"""
        return self.positions[0]
    
    def update(self):
        """Update the snake's position"""
        self.direction = self.next_direction
        head_x, head_y = self.get_head_position()
        
        if self.direction == Direction.UP:
            new_position = (head_x, (head_y - 1) % GRID_HEIGHT)
        elif self.direction == Direction.DOWN:
            new_position = (head_x, (head_y + 1) % GRID_HEIGHT)
        elif self.direction == Direction.LEFT:
            new_position = ((head_x - 1) % GRID_WIDTH, head_y)
        elif self.direction == Direction.RIGHT:
            new_position = ((head_x + 1) % GRID_WIDTH, head_y)
            
        # Check for collision with self
        if new_position in self.positions[1:]:
            return False
            
        self.positions.insert(0, new_position)
        
        if not self.grow_pending:
            self.positions.pop()
        else:
            self.grow_pending = False
            
        return True
    
    def grow(self):
        """Make the snake grow on the next update"""
        self.grow_pending = True
    
    def change_direction(self, new_direction: Direction):
        """Change the snake's direction if valid"""
        # Prevent 180-degree turns
        if (new_direction == Direction.UP and self.direction != Direction.DOWN) or \
           (new_direction == Direction.DOWN and self.direction != Direction.UP) or \
           (new_direction == Direction.LEFT and self.direction != Direction.RIGHT) or \
           (new_direction == Direction.RIGHT and self.direction != Direction.LEFT):
            self.next_direction = new_direction
    
    def draw(self, surface):
        """Draw the snake on the game surface"""
        for i, position in enumerate(self.positions):
            color = GREEN if i == 0 else BLUE  # Head is green, body is blue
            rect = pygame.Rect(
                position[0] * GRID_SIZE, 
                position[1] * GRID_SIZE,
                GRID_SIZE, GRID_SIZE
            )
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)


class Food:
    """Food class that the snake can eat to grow"""
    
    def __init__(self, snake_positions: List[Tuple[int, int]]):
        """Initialize food at a random position not occupied by the snake"""
        self.position = self._get_random_position(snake_positions)
        
    def _get_random_position(self, snake_positions: List[Tuple[int, int]]) -> Tuple[int, int]:
        """Get a random position that's not occupied by the snake"""
        while True:
            position = (
                random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1)
            )
            if position not in snake_positions:
                return position
    
    def draw(self, surface):
        """Draw the food on the game surface"""
        rect = pygame.Rect(
            self.position[0] * GRID_SIZE,
            self.position[1] * GRID_SIZE,
            GRID_SIZE, GRID_SIZE
        )
        pygame.draw.rect(surface, RED, rect)
        pygame.draw.rect(surface, BLACK, rect, 1)


class Game:
    """Main game class"""
    
    def __init__(self):
        """Initialize the game"""
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 24)
        self.reset_game()
        
    def reset_game(self):
        """Reset the game state"""
        self.snake = Snake()
        self.food = Food(self.snake.positions)
        self.score = 0
        self.game_over = False
        self.paused = False
        
    def handle_events(self):
        """Handle game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_r and self.game_over:
                    self.reset_game()
                    
                # Change direction based on arrow keys
                if not self.paused and not self.game_over:
                    if event.key == pygame.K_UP:
                        self.snake.change_direction(Direction.UP)
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction(Direction.DOWN)
                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction(Direction.LEFT)
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction(Direction.RIGHT)
    
    def update(self):
        """Update game state"""
        if self.paused or self.game_over:
            return
            
        # Update snake position
        if not self.snake.update():
            self.game_over = True
            return
            
        # Check for food collision
        if self.snake.get_head_position() == self.food.position:
            self.snake.grow()
            self.food = Food(self.snake.positions)
            self.score += 1
    
    def draw(self):
        """Draw the game"""
        self.screen.fill(WHITE)
        
        # Draw grid
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, GRAY, (0, y), (WINDOW_WIDTH, y))
        
        # Draw snake and food
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        
        # Draw score
        score_text = self.font.render(f'Score: {self.score}', True, BLACK)
        self.screen.blit(score_text, (10, 10))
        
        # Draw game over or paused message
        if self.game_over:
            game_over_text = self.font.render('Game Over! Press R to restart', True, BLACK)
            text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.screen.blit(game_over_text, text_rect)
        elif self.paused:
            paused_text = self.font.render('Paused - Press SPACE to continue', True, BLACK)
            text_rect = paused_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.screen.blit(paused_text, text_rect)
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)


def main():
    """Main function to start the game"""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
