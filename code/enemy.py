import pygame
import random
import time

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
        self.original_position = position  # Store the original position
        self.is_in_jail = False  # Track if the ghost is in jail
        self.jail_time = 0  # Timer to track how long the ghost has been in jail

        # Assign a unique color from the colors list
        self.color = Enemy.colors[Enemy.color_index]
        Enemy.color_index = (Enemy.color_index + 1) % len(Enemy.colors)  # Cycle through colors

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
        self.speed = 3  # Movement speed
        self.current_direction = random.choice(["x", "y"])  # Initial movement direction
        self.current_step = random.choice([-self.speed, self.speed])  # Step size in current direction
        self.direction_timer = 120  # Frames to commit to a direction (increased for smoother movement)
        self.timer_counter = 0  # Timer for tracking frame intervals

    def remove(self, maze):
        """
        Move the ghost to jail and set a timer to free it after 10 seconds.
        The ghost will roam randomly within the '3' cells (jail).
        """
        self.is_in_jail = True
        self.jail_time = time.time()  # Start the timer
        self.jail_cells = self.get_jail_cells(maze)  # Get jail cells from maze
        self.position = random.choice(self.jail_cells)  # Start at a random jail cell
        self.rect.center = self.position  # Update the rect position
        self.current_direction = random.choice(["x", "y"])  # Random direction to roam
        self.move_timer = 0  # Timer for smooth movement
        self.timer_counter = 0  # Reset movement timer

        print(f"{self.color} ghost sent to jail!")

    def get_jail_cells(self, maze):
        """
        Return a list of all coordinates where the maze cell is marked as '3' (the jail).
        """
        jail_cells = []
        for row_idx, row in enumerate(maze.get_layout()):
            for col_idx, cell in enumerate(row):
                if cell == 3:  # Jail cell
                    jail_cells.append((col_idx * maze.cell_size, row_idx * maze.cell_size))
        return jail_cells

    def update(self, maze, player=None, screen=None):
        """
        Update the enemy's position.
        - If the ghost is in jail, roam randomly within neighboring jail cells.
        """
        if self.is_in_jail:
            # Check if 10 seconds have passed
            if time.time() - self.jail_time >= 10:
                self.is_in_jail = False  # Free the ghost
                self.position = self.original_position  # Reset to the original position
                self.rect.center = self.position  # Update the rect position
                print(f"{self.color} ghost freed from jail!")

            # Roam randomly within the jail cells
            else:
                self.move_timer += 1  # Increment move timer

                # Change direction randomly every 120 frames (adjust for smoother movement)
                if self.move_timer >= 120:
                    self.move_timer = 0
                    self.current_direction = random.choice(["x", "y"])  # Randomly pick direction
                    self.current_step = random.choice([-self.speed, self.speed])  # Randomly pick step size

                # Move in the chosen direction
                if self.current_direction == "x":
                    if self.check_jail_boundaries(self.rect.x + self.current_step, self.rect.y, maze):
                        self.rect.x += self.current_step
                elif self.current_direction == "y":
                    if self.check_jail_boundaries(self.rect.x, self.rect.y + self.current_step, maze):
                        self.rect.y += self.current_step

        else:
            if self.timer_counter >= self.direction_timer:
                # Choose a new direction after the timer expires
                self.current_direction = random.choice(["x", "y"])
                self.current_step = random.choice([-self.speed, self.speed])

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

        # Ensure the ghost is drawn at its new position
        if screen:  # Pass the screen object to the draw method
            self.draw(screen)

    def check_jail_boundaries(self, new_x, new_y, maze):
        """
        Check if the new position is within the jail boundaries (i.e., a '3' cell).
        """
        # Convert the new position to the corresponding cell in the maze
        col_idx = new_x // maze.cell_size
        row_idx = new_y // maze.cell_size

        # Check if the new cell is a jail cell (i.e., value '3')
        return maze.layout[row_idx][col_idx] == 3

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
