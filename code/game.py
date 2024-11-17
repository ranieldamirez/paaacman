# game.py
import pygame
from player import Player
from enemy import Enemy
from maze import Maze
from score_manager import ScoreManager
from game_event_manager import GameEventManager
import math
import sys

pygame.init()
# Screen configuration
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600  # screen dimensions
cell_size = 25
FPS = 60  # Frames per second

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 191, 255)

# Fonts
title_font = pygame.font.Font(None, 100)
text_font = pygame.font.Font(None, 36)
small_text_font = pygame.font.Font(None, 28)

# Load the PAAAC-MAN image
try:
    paaacman_image = pygame.image.load("C:/Users/shawn/OneDrive/Pictures/PAAAC.jpg")
    paaacman_image = pygame.transform.scale(paaacman_image, (100, 100))  # Adjust size as needed
except pygame.error:
    print("ERROR: UNABLE TO LOAD THE IMAGE")
    sys.exit()

class GameEngine:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("PAAAC-MAN Arcade Game")
        self.clock = pygame.time.Clock()

        # Initializing game elements
        self.map = Maze(SCREEN_WIDTH, SCREEN_HEIGHT, cell_size)
        self.player = Player(cell_size, self.map)
        self.ghosts = [Enemy(cell_size, self.map) for _ in range(4)]  # Instantiate 4 ghost enemies
        self.score_manager = ScoreManager()
        self.event_manager = GameEventManager()

        self.running = True
        self.state = "start_menu"  # Initializing to start menu
        self.ghost_speed = 5  # Adjust the ghost speed to slow it down (higher value = slower)

    # Start menu state
    def start_menu(self):
        # Display start menu
        self.screen.fill(BLACK)
        title_text = title_font.render("PAAC-MAN", True, YELLOW)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 4))
        self.screen.blit(title_text, title_rect)

        # Display the paacman image next to title
        image_x = title_rect.right + 20  # Position the image to the right of the title
        image_y = title_rect.centery - paaacman_image.get_height() // 2
        self.screen.blit(paaacman_image, (image_x, image_y))

        # Display High Scores
        high_scores = ScoreManager.getInstance().get_high_scores()  # Get high scores
        for i, (username, score) in enumerate(high_scores):
            score_text = text_font.render(f"{i + 1}. {username}: {score}", True, WHITE)
            self.screen.blit(score_text, (self.screen.get_width() // 3, (self.screen.get_height() // 2) + i * 40))

        # Display Credits
        credits_text = small_text_font.render("© 2024 CPSC 6119 Team 4", True, WHITE)
        self.screen.blit(credits_text, (SCREEN_WIDTH // 2 - credits_text.get_width() // 2, SCREEN_HEIGHT - 50))

        # Waiting for player to press a key to start
        font = pygame.font.Font(None, 36)  # Set font size
        prompt = font.render("Press any key to start", True, WHITE)
        self.screen.blit(prompt, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2 - 50))  # Draw onto screen
        pygame.display.flip()  # Update screen contents

        # Check if user pressed down on a key
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.state = "playing"
            elif event.type == pygame.QUIT:
                self.running = False

    # Game over state
    def game_over_screen(self):
        # Display 'game over' screen
        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        message = font.render("Game Over", True, (255, 0, 0))
        self.screen.blit(message, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3))  # Draw onto screen

        pygame.display.flip()
        pygame.time.wait(3000)  # Show 'game over' screen for 5 seconds
        self.running = False  # End game

    def main_game(self):
        # Clear the screen
        self.screen.fill(BLACK)

        # Draw the maze layout
        self.map.draw(self.screen)

        # Update and draw the player
        self.player.update(self.map)
        self.player.collect_pellet(self.map)
        self.player.draw(self.screen)

        # Update and draw the ghosts
        for ghost in self.ghosts:
            if pygame.time.get_ticks() % self.ghost_speed == 0:  # Slow down ghost updates
                ghost.update(self.map, self.player)
            ghost.draw(self.screen)

        # Display the score
        score_text = text_font.render(f"Score: {self.score_manager.getInstance().get_current_score()}", True, WHITE)
        self.screen.blit(score_text, (10, 10))  # Top-left corner

        # Check for game over conditions
        if self.player.collides_with_ghost(self.ghosts):
            self.state = "game_over"
        elif self.map.all_pellets_collected():
            self.state = "game_over"

        # Update the display
        pygame.display.flip()

        # Handle user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.state = "game_over"

    def run(self):
        while self.running:
            # Clear events at the start of each frame
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # Handle global key press for quitting
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False

                # Pass event to the current state
                if self.state == "start_menu":
                    if event.type == pygame.KEYDOWN:
                        self.state = "playing"

                # If you pause while playing // **** add pausing functionality later ****  
                elif self.state == "playing":
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.state = "game_over"

            # Render based on current state
            if self.state == "start_menu":
                self.start_menu()
            elif self.state == "playing":
                self.main_game()
            elif self.state == "game_over":
                self.game_over_screen()

            self.clock.tick(FPS)  # Limit the frame rate

        pygame.quit()


if __name__ == "__main__":
    game = GameEngine()
    game.run()
