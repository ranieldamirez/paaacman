import pygame
from observer_pattern import Subject
from SuperPlayerDecorator import SuperPlayerDecorator

class Player(Subject):
    def __init__(self, cell_size, maze, start_position=None):
        super().__init__()
        if start_position is None:
            # Find the first walkable cell in the maze (a cell with value 0)
            for row_idx, row in enumerate(maze.get_layout()):
                for col_idx, cell in enumerate(row):
                    if cell == 0:  # Walkable pathway
                        start_position = (col_idx * cell_size, row_idx * cell_size)
                        break
                if start_position:
                    break

        self.position = list(start_position)
        self.cell_size = cell_size
        self.speed = 5
        self.current_direction = None
        self.next_direction = None

        try:
            self.image = pygame.image.load(r"./resources/pacman.png")
            self.image = pygame.transform.scale(self.image, (cell_size, cell_size))
        except pygame.error:
            self.image = pygame.Surface((cell_size, cell_size))
            self.image.fill((255, 255, 0))

        self.rect = self.image.get_rect(center=(self.position[0] + self.cell_size // 2,
                                                 self.position[1] + self.cell_size // 2))

    def update(self, maze, ghosts=None):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.next_direction = (-self.speed, 0)
        elif keys[pygame.K_RIGHT]:
            self.next_direction = (self.speed, 0)
        elif keys[pygame.K_UP]:
            self.next_direction = (0, -self.speed)
        elif keys[pygame.K_DOWN]:
            self.next_direction = (0, self.speed)

        sub_steps = self.speed
        for _ in range(sub_steps):
            if self.next_direction and self.is_close_to_grid():
                proposed_rect = self.rect.move(self.next_direction[0] // sub_steps,
                                               self.next_direction[1] // sub_steps)

                col_idx = proposed_rect.x // maze.cell_size
                row_idx = proposed_rect.y // maze.cell_size

                if maze.layout[row_idx][col_idx] != 3:
                    if not self.check_wall_collision(maze, proposed_rect):
                        self.current_direction = self.next_direction
                        self.next_direction = None

            if self.current_direction:
                proposed_rect = self.rect.move(self.current_direction[0] // sub_steps,
                                               self.current_direction[1] // sub_steps)

                col_idx = proposed_rect.x // maze.cell_size
                row_idx = proposed_rect.y // maze.cell_size

                if maze.layout[row_idx][col_idx] != 3:
                    if not self.check_wall_collision(maze, proposed_rect):
                        self.rect = proposed_rect

        return self

    def collides_with_ghost(self, ghosts):
        """
        Check if the player collides with any ghosts.
        """
        for ghost in ghosts:
            if self.rect.colliderect(ghost.rect):
                # Notify observers about the collision
                self.notify_observers("player_collided_with_ghost", {"player": self, "ghost": ghost})
                return True  # Collision detected
        return False  # No collision with ghosts



    def collect_pellet(self, maze):
        for pellet in maze.pellets:
            if self.rect.collidepoint(pellet):
                maze.pellets.remove(pellet)
                col_idx = (pellet[0] - maze.cell_size // 2) // maze.cell_size
                row_idx = (pellet[1] - maze.cell_size // 2) // maze.cell_size

                if maze.layout[row_idx][col_idx] == 2:
                    self.notify_observers("super_pellet_collected", {"player": self, "pellet_position": pellet})
                    return SuperPlayerDecorator(self)

                self.notify_observers("pellet_collected", {"player": self, "pellet_position": pellet})
                return self
        return self

    def snap_to_grid(self, maze):
        """Align the character's position to the grid."""
        self.rect.x = (self.rect.x // maze.cell_size) * maze.cell_size
        self.rect.y = (self.rect.y // maze.cell_size) * maze.cell_size


    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_close_to_grid(self, threshold=5):
        x_offset = self.rect.x % self.cell_size
        y_offset = self.rect.y % self.cell_size
        return (x_offset < threshold or x_offset > self.cell_size - threshold) and \
               (y_offset < threshold or y_offset > self.cell_size - threshold)

    def check_wall_collision(self, maze, proposed_rect=None):
        rect_to_check = proposed_rect if proposed_rect else self.rect
        for wall in maze.walls:
            if rect_to_check.colliderect(wall):
                return True
        return False
