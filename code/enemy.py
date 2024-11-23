import pygame
import random

class Enemy:
    colors = [(255, 0, 0), (255, 192, 203), (0, 255, 0), (0, 0, 255)]  # Red, Pink, Green, Blue
    color_index = 0  # Tracks the next color to assign

    def __init__(self, cell_size, maze, position=None):
        if position is None:
            # Find a random walkable cell in the maze
            walkable_cells = [(col_idx * maze.cell_size, row_idx * maze.cell_size)
                              for row_idx, row in enumerate(maze.layout)
                              for col_idx, cell in enumerate(row) if cell == 0]
            position = random.choice(walkable_cells)

        self.cell_size = cell_size
        self.position = position
        self.in_jail = False
        self.jail_timer = 0  # Timer for tracking jail duration (in frames)
        self.maze = maze

        # Assign a unique color from the colors list
        self.color = Enemy.colors[Enemy.color_index]
        Enemy.color_index = (Enemy.color_index + 1) % len(Enemy.colors)

        # Load images for specific colors
        if self.color == (255, 0, 0):  # Red ghost
            try:
                self.image = pygame.image.load(r"./resources/yellow.png")
                self.image = pygame.transform.scale(self.image, (cell_size, cell_size))  # Scale the image to fit
            except pygame.error:
                print("Error loading yellow ghost image, defaulting to red color.")
                self.image = pygame.Surface((cell_size, cell_size))
                self.image.fill(self.color)
        elif self.color == (0, 255, 0):  # Green ghost
            try:
                self.image = pygame.image.load(r"./resources/Green.png")
                self.image = pygame.transform.scale(self.image, (cell_size, cell_size))  # Scale the image to fit
            except pygame.error:
                print("Error loading green ghost image, defaulting to color.")
                self.image = pygame.Surface((cell_size, cell_size))
                self.image.fill(self.color)
        elif self.color == (255, 192, 203):  # Pink ghost
            try:
                self.image = pygame.image.load(r"./resources/pink.png")
                self.image = pygame.transform.scale(self.image, (cell_size, cell_size))  # Scale the image to fit
            except pygame.error:
                print("Error loading pink ghost image, defaulting to color.")
                self.image = pygame.Surface((cell_size, cell_size))
                self.image.fill(self.color)
        elif self.color == (0, 0, 255):  # Blue ghost
            try:
                self.image = pygame.image.load(r"./resources/blue.png")
                self.image = pygame.transform.scale(self.image, (cell_size, cell_size))  # Scale the image to fit
            except pygame.error:
                print("Error loading blue ghost image, defaulting to color.")
                self.image = pygame.Surface((cell_size, cell_size))
                self.image.fill(self.color)
        else:
            # Default appearance for other ghosts
            self.image = pygame.Surface((cell_size, cell_size))
            self.image.fill(self.color)

        self.rect = self.image.get_rect(center=(self.position[0] + maze.cell_size // 2,
                                                 self.position[1] + maze.cell_size // 2))
        self.speed = 3
        self.current_direction = random.choice(["x", "y"])
        self.current_step = random.choice([-self.speed, self.speed])
        self.direction_timer = 60
        self.timer_counter = 0

    def update(self, maze, player=None):
        if self.in_jail:
            self.handle_jail()
        else:
            self.move_normal(maze)

    def move_normal(self, maze):
        """Normal movement outside jail."""
        self.timer_counter += 1
        if self.timer_counter >= self.direction_timer:
            # Change direction after timer expires
            self.current_direction = random.choice(["x", "y"])
            self.current_step = random.choice([-self.speed, self.speed])
            self.timer_counter = 0

        if self.current_direction == "x":
            self.rect.x += self.current_step
            if self.check_wall_collision(maze):
                self.rect.x -= self.current_step
                self.timer_counter = self.direction_timer
        elif self.current_direction == "y":
            self.rect.y += self.current_step
            if self.check_wall_collision(maze):
                self.rect.y -= self.current_step
                self.timer_counter = self.direction_timer

    def handle_jail(self):
        """Movement restricted to jail cells and handling release after timer."""
        self.jail_timer += 1
        if self.jail_timer >= 600:  # 10 seconds in jail
            # Move to the cell above the jail
            self.rect.y -= self.cell_size
            self.in_jail = False
            self.jail_timer = 0
            return

        # Jail movement: restricted to '3' cells
        self.timer_counter += 1
        if self.timer_counter >= self.direction_timer:
            self.current_direction = random.choice(["x", "y"])
            self.current_step = random.choice([-self.speed, self.speed])
            self.timer_counter = 0

        if self.current_direction == "x":
            self.rect.x += self.current_step
            if not self.check_jail_collision():
                self.rect.x -= self.current_step
                self.timer_counter = self.direction_timer
        elif self.current_direction == "y":
            self.rect.y += self.current_step
            if not self.check_jail_collision():
                self.rect.y -= self.current_step
                self.timer_counter = self.direction_timer

    def check_wall_collision(self, maze):
        """Check collision with walls outside the jail."""
        for wall in maze.walls:
            if self.rect.colliderect(wall):
                return True
        return False

    def check_jail_collision(self):
        """Check if the ghost is within valid '3' jail cells."""
        col = self.rect.x // self.cell_size
        row = self.rect.y // self.cell_size
        return self.maze.layout[row][col] == 3

    def remove(self, maze):
        """Send ghost to the nearest jail cell."""
        self.in_jail = True
        self.jail_timer = 0

        # Find the first jail cell ('3') in the maze layout
        for row_idx, row in enumerate(maze.layout):
            for col_idx, cell in enumerate(row):
                if cell == 3:
                    self.rect.topleft = (col_idx * self.cell_size, row_idx * self.cell_size)
                    return

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def get_position(self):
        return self.rect.topleft
