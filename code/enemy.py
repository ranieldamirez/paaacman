import pygame
import random
from observer_pattern import Subject

class Enemy(Subject):
    colors = [(255, 0, 0), (255, 192, 203), (0, 255, 0), (0, 0, 255)]  # Red, Pink, Green, Blue
    color_index = 0

    def __init__(self, cell_size, maze, position=None, strategy=None):
        super().__init__()
        if position is None:
            walkable_cells = [(col_idx * maze.cell_size, row_idx * maze.cell_size)
                              for row_idx, row in enumerate(maze.layout)
                              for col_idx, cell in enumerate(row) if cell == 0]
            position = random.choice(walkable_cells)
        self.cell_size = cell_size
        self.maze = maze
        self.in_jail = False
        self.jail_timer = 0

        # Initialize movement attributes
        self.timer_counter = 0  # Counts frames to control movement direction change
        self.direction_timer = 60  # Frames to wait before changing direction
        self.speed = 3
        self.current_direction = random.choice(["x", "y"])  # Direction: "x" or "y"
        self.current_step = random.choice([-self.speed, self.speed])  # Movement step: positive or negative
        
        self.strategy = strategy if strategy else RandomMovement()

        self.position = position
        self.color = Enemy.colors[Enemy.color_index]
        Enemy.color_index = (Enemy.color_index + 1) % len(Enemy.colors)

        try:
            self.image = pygame.image.load(f"./resources/ghost_{Enemy.color_index}.png")
            self.image = pygame.transform.scale(self.image, (cell_size, cell_size))
        except pygame.error:
            self.image = pygame.Surface((cell_size, cell_size))
            self.image.fill(self.color)

        self.rect = self.image.get_rect(center=(self.position[0] + maze.cell_size // 2,
                                                 self.position[1] + maze.cell_size // 2))

    def update(self, maze, player=None):
        if self.in_jail:
            self.handle_jail(maze)
        else:
            self.strategy.move(self, maze, player)

    def handle_jail(self, maze):
        """Movement restricted to jail cells and handling release after timer."""
        self.jail_timer += 1
        if self.jail_timer >= 600:  # 10 seconds in jail
            # Find the '4' cell in the maze for respawn
            for row_idx, row in enumerate(maze.layout):
                for col_idx, cell in enumerate(row):
                    if cell == 4:  # Respawn point
                        # Move to the cell above the jail
                        self.rect.center = (
                            col_idx * maze.cell_size + maze.cell_size // 2,
                            row_idx * maze.cell_size + maze.cell_size // 2
                        )
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

    def check_jail_collision(self):
        col = self.rect.centerx // self.cell_size
        row = self.rect.centery // self.cell_size

        if 0 <= row < len(self.maze.layout) and 0 <= col < len(self.maze.layout[row]):
            is_valid = self.maze.layout[row][col] == 3
            return is_valid
        return False
    
    def check_wall_or_restricted_cell(self, maze):
        """
        Check if the ghost collides with walls or restricted '3' cells.
        Ghosts avoid '3' cells unless they are in jail.
        """
        # Check wall collision
        for wall in maze.walls:
            if self.rect.colliderect(wall):
                return True

        # Check if the ghost is moving into a '3' cell
        col = self.rect.centerx // self.cell_size
        row = self.rect.centery // self.cell_size
        if not self.in_jail and maze.layout[row][col] == 3:
            return True

        return False


    def remove(self, maze):
        self.in_jail = True
        self.jail_timer = 0

        for row_idx, row in enumerate(maze.layout):
            for col_idx, cell in enumerate(row):
                if cell == 3:
                    self.rect.topleft = (col_idx * self.cell_size, row_idx * self.cell_size)
                    return

    def set_scared(self):
        """Change the ghost's appearance to the scared look."""
        try:
            self.image = pygame.image.load(r"./resources/scared_ghost.png")
            self.image = pygame.transform.scale(self.image, (self.cell_size, self.cell_size))
        except pygame.error:
            print("Error loading scared ghost image. Retaining current appearance.")

    def reset_appearance(self):
        """Reset the ghost's appearance to its original look."""
        # Reload the image based on the assigned color
        try:
            if self.color == (255, 0, 0):  # Red ghost
                self.image = pygame.image.load(r"./resources/ghost_0.png")
            elif self.color == (0, 255, 0):  # Green ghost
                self.image = pygame.image.load(r"./resources/ghost_1.png")
            elif self.color == (255, 192, 203):  # Pink ghost
                self.image = pygame.image.load(r"./resources/ghost_2.png")
            elif self.color == (0, 0, 255):  # Blue ghost
                self.image = pygame.image.load(r"./resources/ghost_3.png")
            self.image = pygame.transform.scale(self.image, (self.cell_size, self.cell_size))
        except pygame.error:
            print("Error resetting ghost appearance. Retaining current look.")


    def draw(self, screen):
        screen.blit(self.image, self.rect)
