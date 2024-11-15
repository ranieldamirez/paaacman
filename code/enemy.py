# enemy.py
import pygame
import random

class Enemy:
    def __init__(self, cell_size, maze, position=None):
        """
        Initialize the enemy with a valid starting position in a walkable cell.
        """
        if position is None:
            # Find a random walkable cell in the maze
            walkable_cells = []
            for row_idx, row in enumerate(maze.layout):
                for col_idx, cell in enumerate(row):
                    if cell == 0:  # Walkable pathway
                        walkable_cells.append((col_idx * maze.cell_size, row_idx * maze.cell_size))

            # Choose a random walkable cell
            position = random.choice(walkable_cells)

        self.position = position
        self.image = pygame.Surface((20, 20))  # Placeholder for enemy appearance
        self.image.fill((255, 0, 0))  # Red color for enemy
        self.rect = self.image.get_rect(center=(self.position[0] + maze.cell_size // 2, 
                                                 self.position[1] + maze.cell_size // 2))
        self.speed = 4  # Movement speed
        self.current_direction = random.choice(["x", "y"])  # Initial movement direction
        self.current_step = random.choice([-self.speed, self.speed])  # Step size in current direction
        self.direction_timer = 60  # Frames to commit to a direction (adjust as needed)
        self.timer_counter = 0

    def update(self, maze, player=None):
        """
        Update the enemy's position.
        - Commit to a direction for a fixed duration before changing.
        - Avoid walls.
        """
        if self.timer_counter >= self.direction_timer:
            # Choose a new direction after the timer expires
            self.current_direction = random.choice(["x", "y"])
            self.current_step = random.choice([-self.speed, self.speed])
            self.timer_counter = 0  # Reset timer

        # Try moving in the committed direction
        if self.current_direction == "x":
            self.rect.x += self.current_step
            if self.check_wall_collision(maze):
                self.rect.x -= self.current_step
                self.timer_counter = self.direction_timer  # Force direction change
        elif self.current_direction == "y":
            self.rect.y += self.current_step
            if self.check_wall_collision(maze):
                self.rect.y -= self.current_step
                self.timer_counter = self.direction_timer  # Force direction change

        self.timer_counter += 1  # Increment timer counter

    def check_wall_collision(self, maze):
        """
        Check if the enemy collides with any walls in the maze.
        """
        for wall in maze.walls:
            if self.rect.colliderect(wall):
                return True
        return False

    def draw(self, screen):
        """
        Draw the enemy on the screen.
        """
        screen.blit(self.image, self.rect)

    def get_position(self):
        """
        Get the current position of the enemy.
        """
        return self.rect.topleft
