import pygame

class SuperPlayerDecorator:
    def __init__(self, player):
        """
        Decorate the player to enhance behavior after eating a super-pellet.
        """
        self.originalPlayer = player  # Keep track of the original player
        self.player = player
        self.super_mode_timer = 300  # Super mode duration (e.g., 300 frames)

    def __getattr__(self, name):
        """
        Delegate access to attributes and methods to the wrapped Player instance.
        """
        return getattr(self.player, name)

    def update(self, maze, ghosts):
        self.super_mode_timer -= 1  # Countdown timer for super mode

        # Temporarily increase speed
        if not hasattr(self.player, "_original_speed"):  # Save the original speed only once
            self.player._original_speed = self.player.speed
        self.player.speed = 5  # Enhanced speed for super mode

        # Delegate normal update logic to the original player
        self.player.update(maze, ghosts)

        # Handle ghost interactions (e.g., send ghosts to jail)
        for ghost in ghosts:
            if self.player.rect.colliderect(ghost.rect):
                ghost.remove(maze)  # Place the ghost in jail
                print("Ghost eaten!")  # Debug info

        # Revert to the original player if the timer expires
        if self.super_mode_timer <= 0:
            # Restore player state and remove decorator
            self.player.speed = self.player._original_speed  # Restore original speed
            del self.player._original_speed  # Clean up temporary attribute
            self.player.image = pygame.image.load(r"./resources/pacman.png")
            self.player.image = pygame.transform.scale(self.player.image, (self.player.cell_size, self.player.cell_size))  # Reset image size
            print("Super mode ended, reverting to normal player.")  # Debug info
            return self.originalPlayer  # Return to the original player state

        return self  # Keep the decorator active while in super mode

    def collect_pellet(self, maze):
        """
        Delegate pellet collection to the wrapped player.
        """
        return self.player.collect_pellet(maze)

    def draw(self, screen):
        """
        Draw the player (unchanged).
        """
        screen.blit(self.player.image, self.player.rect)
