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
        self.player.speed = 4  # Enhanced speed for super mode
        self.player.image.fill((255, 255, 0))  # Change color to yellow (for super mode)

        self.player.update(maze, ghosts)  # Delegate update to the player

        # Handle ghost interactions
        for ghost in ghosts:
            if self.player.rect.colliderect(ghost.rect):
                # Place the ghost in jail
                ghost.remove(maze)  # Pass the maze to the `remove()` method
                print("Ghost eaten!")  # Debug info

        # Revert to the original player if the timer expires
        if self.super_mode_timer <= 0:
            print("Super mode ended, reverting to normal player.")  # Debug info
            self.player.image = pygame.image.load(r"./resources/pacman.png")
            self.player.image = pygame.transform.scale(self.player.image, (self.player.cell_size, self.player.cell_size))  # Reset image size
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
