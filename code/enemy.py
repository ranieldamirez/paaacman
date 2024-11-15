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

    def update(self, maze, player=None):
        """
        Update the enemy's position.
        - Movement is random for now but avoids walls.
        - Can be extended to chase the player.
        """
        # Random direction: horizontal or vertical
        direction = random.choice(["x", "y"])
        step = random.choice([-self.speed, self.speed])
        
        # Try moving in the chosen direction
        if direction == "x":
            self.rect.x += step
            # Revert if colliding with a wall
            if self.check_wall_collision(maze):
                self.rect.x -= step
        elif direction == "y":
            self.rect.y += step
            # Revert if colliding with a wall
            if self.check_wall_collision(maze):
                self.rect.y -= step

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
