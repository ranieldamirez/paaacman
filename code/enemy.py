# enemy.py
import pygame
import random

class Enemy:
    colors = [(255, 0, 0), (255, 192, 203), (0, 255, 0), (0, 0, 255)]  # Red, Pink, Green, Blue
    color_index = 0  # Tracks the next color to assign

    def __init__(self, cell_size, maze, position=None):
        """
        Initialize the enemy with a valid starting position in a walkable cell and assign a unique color or image.
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

        # Assign a unique color from the colors list
        self.color = Enemy.colors[Enemy.color_index]
        Enemy.color_index = (Enemy.color_index + 1) % len(Enemy.colors)  # Cycle through colors

        # Load images for specific colors
        if self.color == (255, 0, 0):  # Red ghost
            try:
                self.image = pygame.image.load(r"./resources/yellow.png")
                self.image = pygame.transform.scale(self.image, (20, 20))  # Scale the image to fit
            except pygame.error:
                print("Error loading yellow ghost image, defaulting to red color.")
                self.image = pygame.Surface((20, 20))
                self.image.fill(self.color)
        elif self.color == (0, 255, 0):  # Green ghost
            try:
                self.image = pygame.image.load(r"./resources/Green.png")
                self.image = pygame.transform.scale(self.image, (20, 20))  # Scale the image to fit
            except pygame.error:
                print("Error loading green ghost image, defaulting to color.")
                self.image = pygame.Surface((20, 20))
                self.image.fill(self.color)
        elif self.color == (255, 192, 203):  # Pink ghost
            try:
                self.image = pygame.image.load(r"./resources/pink.png")
                self.image = pygame.transform.scale(self.image, (20, 20))  # Scale the image to fit
            except pygame.error:
                print("Error loading pink ghost image, defaulting to color.")
                self.image = pygame.Surface((20, 20))
                self.image.fill(self.color)
        elif self.color == (0, 0, 255):  # Blue ghost
            try:
                self.image = pygame.image.load(r"./resources/blue.png")
                self.image = pygame.transform.scale(self.image, (20, 20))  # Scale the image to fit
            except pygame.error:
                print("Error loading blue ghost image, defaulting to color.")
                self.image = pygame.Surface((20, 20))
                self.image.fill(self.color)
        else:
            # Default appearance for other ghosts
            self.image = pygame.Surface((20, 20))
            self.image.fill(self.color)

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
