import pygame
from score_manager import ScoreManager
from SuperPlayerDecorator import SuperPlayerDecorator

class Player:
    def __init__(self, cell_size, maze, start_position=None):
        """
        Initialize the player with a starting position, ensuring it's in a valid pathway.
        """
        if start_position is None:
            # Find the first walkable cell in the maze (a cell with value 0)
            for row_idx, row in enumerate(maze.get_layout()):
                for col_idx, cell in enumerate(row):
                    if cell == 0:  # Walkable pathway
                        start_position = (col_idx * cell_size, row_idx * cell_size)
                        break
                if start_position:
                    break

        self.position = list(start_position)  # Player's starting position
        self.cell_size = cell_size
        self.speed = 3  # Movement speed
        self.current_direction = None  # Current direction of movement
        self.next_direction = None  # Next direction pressed by player

        # Load the Paac-Man image
        try:
            self.image = pygame.image.load(r"./resources/pacman.png")
            self.image = pygame.transform.scale(self.image, (cell_size, cell_size))  # Scale the image to fit
        except pygame.error:
            print("Error loading Paac-Man image, defaulting to yellow color.")
            self.image = pygame.Surface((cell_size, cell_size))  # Fallback appearance
            self.image.fill((255, 255, 0))  # Yellow color as fallback

        self.rect = self.image.get_rect(center=(self.position[0] + self.cell_size // 2,
                                                 self.position[1] + self.cell_size // 2))

    def update(self, maze, ghosts=None):
        """
        Update the player's position with sub-step movement to avoid skipping rows.
        """
        # Handle user input for the next direction
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.next_direction = (-self.speed, 0)  # Move left
        elif keys[pygame.K_RIGHT]:
            self.next_direction = (self.speed, 0)  # Move right
        elif keys[pygame.K_UP]:
            self.next_direction = (0, -self.speed)  # Move up
        elif keys[pygame.K_DOWN]:
            self.next_direction = (0, self.speed)  # Move down

        # Break movement into sub-steps for collision checking
        sub_steps = self.speed  # Number of sub-steps
        for _ in range(sub_steps):
            if self.next_direction and self.is_close_to_grid():
                # Calculate the proposed position after movement
                proposed_rect = self.rect.move(self.next_direction[0] // sub_steps, self.next_direction[1] // sub_steps)

                # Get the grid position the player is trying to move into
                col_idx = proposed_rect.x // maze.cell_size
                row_idx = proposed_rect.y // maze.cell_size

                # Check if the player is trying to move into a restricted cell (cell with value 3)
                if maze.layout[row_idx][col_idx] != 3:  # If not a restricted cell
                    if not self.check_wall_collision(maze, proposed_rect):  # Make sure there's no wall collision
                        self.current_direction = self.next_direction  # Update direction
                        self.next_direction = None  # Clear next direction

            # Apply the movement if valid
            if self.current_direction:
                proposed_rect = self.rect.move(self.current_direction[0] // sub_steps, self.current_direction[1] // sub_steps)
                col_idx = proposed_rect.x // maze.cell_size
                row_idx = proposed_rect.y // maze.cell_size

                # Only move if the target cell is not restricted (cell with value 3)
                if maze.layout[row_idx][col_idx] != 3:  # Check if not restricted (cell 3)
                    if not self.check_wall_collision(maze, proposed_rect):
                        self.rect = proposed_rect  # Move the player
                    else:
                        self.current_direction = None  # Stop movement if blocked
                else:
                    # Prevent movement if trying to enter the ghost jail
                    self.current_direction = None  # Stop movement
        return self

        
    def is_close_to_grid(self, threshold=5):
        """
        Check if the player is close enough to the center of the current grid cell.
        """
        x_offset = self.rect.x % self.cell_size
        y_offset = self.rect.y % self.cell_size
        return (x_offset < threshold or x_offset > self.cell_size - threshold) and \
            (y_offset < threshold or y_offset > self.cell_size - threshold)



    def check_wall_collision(self, maze, proposed_rect=None):
        """
        Check if the player collides with any walls in the maze.
        """
        rect_to_check = proposed_rect if proposed_rect else self.rect
        for wall in maze.walls:
            if rect_to_check.colliderect(wall):
                return True  # Collision detected
        return False  # No collision


    def collides_with_ghost(self, ghosts):
        """
        Check if the player collides with any ghosts.
        """
        for ghost in ghosts:
            if self.rect.colliderect(ghost.rect):
                return True  # Collision detected with a ghost
        return False  # No collision with ghosts

    def collect_pellet(self, maze):
        """
        Check if the player collects a pellet, and remove it from the maze if collected.
        """
        for pellet in maze.pellets:
            if self.rect.collidepoint(pellet):  # Check if the player's rect overlaps the pellet position
                maze.pellets.remove(pellet)  # Remove the pellet from the maze
                col_idx = (pellet[0] - maze.cell_size // 2) // maze.cell_size
                row_idx = (pellet[1] - maze.cell_size // 2) // maze.cell_size

                # Check if it's a super-pellet
                if maze.layout[row_idx][col_idx] == 2:
                    print("Super-pellet collected!")  # Debug info (optional)
                    return SuperPlayerDecorator(self)  # Return a decorated player
                
                ScoreManager.getInstance().add_score(10)  # Add points for normal pellet
                return self  # Return the same player
        return self  # No pellet collected

    def draw(player, screen):
        """
        Draw the player on the screen.
        """
        screen.blit(player.image, player.rect)

    def set_speed(self, speed):
        """
        Set the player speed.
        """
        self.speed = speed
