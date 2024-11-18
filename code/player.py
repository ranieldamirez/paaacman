import pygame
from score_manager import ScoreManager

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
        self.speed = 2  # Movement speed
        self.current_direction = None  # Current direction of movement
        self.next_direction = None  # Next direction pressed by player

        # Load the Paac-Man image
        try:
            self.image = pygame.image.load(r"./resources/pacman.png")
            self.image = pygame.transform.scale(self.image, (20, 20))  # Scale the image to fit
        except pygame.error:
            print("Error loading Paac-Man image, defaulting to yellow color.")
            self.image = pygame.Surface((20, 20))  # Fallback appearance
            self.image.fill((255, 255, 0))  # Yellow color as fallback

        self.rect = self.image.get_rect(center=(self.position[0] + self.cell_size // 2,
                                                 self.position[1] + self.cell_size // 2))

    def update(self, maze):
        """
        Update the player's position based on the last direction and handle wall collisions.
        """
        keys = pygame.key.get_pressed()
        
        # Update the next direction based on key press
        if keys[pygame.K_LEFT]:
            self.next_direction = (-self.speed, 0)  # Move left
        elif keys[pygame.K_RIGHT]:
            self.next_direction = (self.speed, 0)  # Move right
        elif keys[pygame.K_UP]:
            self.next_direction = (0, -self.speed)  # Move up
        elif keys[pygame.K_DOWN]:
            self.next_direction = (0, self.speed)  # Move down

        # Attempt to move in the next direction if it's set
        if self.next_direction:
            self.rect.x += self.next_direction[0]
            self.rect.y += self.next_direction[1]

            if not self.check_wall_collision(maze):
                self.current_direction = self.next_direction  # Update the current direction
                self.next_direction = None  # Clear the next direction
            else:
                # Revert the attempted move
                self.rect.x -= self.next_direction[0]
                self.rect.y -= self.next_direction[1]

        # Continue moving in the current direction
        if self.current_direction:
            self.rect.x += self.current_direction[0]
            self.rect.y += self.current_direction[1]

            if self.check_wall_collision(maze):
                # Revert the movement if colliding with a wall
                self.rect.x -= self.current_direction[0]
                self.rect.y -= self.current_direction[1]

    def check_wall_collision(self, maze):
        """
        Check if the player collides with any walls in the maze.
        """
        for wall in maze.walls:
            if self.rect.colliderect(wall):
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
                ScoreManager.getInstance().add_score(10)  # Add points for collecting a pellet
                return True  # Pellet collected
        return False  # No pellet collected

    def draw(self, screen):
        """
        Draw the player on the screen.
        """
        screen.blit(self.image, self.rect)

    def set_speed(self, speed):
        """
        Set the player speed.
        """
        self.speed = speed
