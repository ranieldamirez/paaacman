import pygame
from observer_pattern import Subject

class SuperPlayerDecorator(Subject):
    def __init__(self, player):
        super().__init__()
        self.originalPlayer = player  # Reference to the original player
        self.player = player
        self.super_mode_timer = 300  # Duration of super mode (e.g., 300 frames)

    def __getattr__(self, name):
        return getattr(self.player, name)

    def update(self, maze, ghosts):
        self.super_mode_timer -= 1

        # Temporarily increase speed
        if not hasattr(self.player, "_original_speed"):
            self.player._original_speed = self.player.speed
        self.player.speed = 5

        # Delegate update logic to the wrapped player
        self.player.update(maze, ghosts)

        # Handle ghost collisions
        for ghost in ghosts:
            if self.player.rect.colliderect(ghost.rect):
                self.notify_observers("ghost_eaten", {"ghost": ghost})
                ghost.remove(maze)

        # Revert to the original player if timer expires
        if self.super_mode_timer <= 0:
            self.player.speed = self.player._original_speed  # Restore original speed
            del self.player._original_speed  # Clean up attribute
            return self.originalPlayer

        return self

    def collect_pellet(self, maze):
        return self.player.collect_pellet(maze)

    def draw(self, screen):
        screen.blit(self.player.image, self.player.rect)
