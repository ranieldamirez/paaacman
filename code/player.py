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
        self.image = pygame.Surface((20, 20))  # Placeholder for player appearance
        self.image.fill((255, 255, 0))  # Yellow color for Paac-Man
        self.rect = self.image.get_rect(center=(self.position[0] + cell_size // 2, 
                                                 self.position[1] + cell_size // 2))
        self.speed = 5  # Movement speed


    def update(self, maze):
        """
        Update the player's position based on keyboard input and handle wall collisions.
        """
        keys = pygame.key.get_pressed()
        
        # Movement in the X direction
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            if self.check_wall_collision(maze):
                self.rect.x += self.speed  # Undo movement if colliding with a wall
        elif keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            if self.check_wall_collision(maze):
                self.rect.x -= self.speed  # Undo movement if colliding with a wall
        
        # Movement in the Y direction
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
            if self.check_wall_collision(maze):
                self.rect.y += self.speed  # Undo movement if colliding with a wall
        elif keys[pygame.K_DOWN]:
            self.rect.y += self.speed
            if self.check_wall_collision(maze):
                self.rect.y -= self.speed  # Undo movement if colliding with a wall

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
