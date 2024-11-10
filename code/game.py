# game.py
import pygame
from player import Player
from enemy import Enemy
from maze import Maze
from score_manager import ScoreManager
from game_event_manager import GameEventManager
import sys

pygame.init()
# Screen configuration
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600 # screen dimensions
FPS = 60 # Frames per second

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
    paaacman_image = pygame.image.load("./resources/PAAAC.jpg")
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
        self.player = Player()
        self.ghosts = [Enemy() for _ in range(4)] # Instantiate 4 ghost enemies
        self.map = Maze()
        self.score_manager = ScoreManager()
        self.event_manager = GameEventManager()

        self.running = True
        self.state = "start_menu" #initializing to start menu

# start menu state
    def start_menu(self):

        # display start menu
        self.screen.fill(BLACK)
        title_text = title_font.render("PAAC-MAN", True, YELLOW)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 4))
        self.screen.blit(title_text, title_rect)

        # Display the paacman image next to title
        image_x = title_rect.right + 20  # Position the image to the right of the title
        image_y = title_rect.centery - paaacman_image.get_height() // 2
        self.screen.blit(paaacman_image, (image_x, image_y))

        # Display High Scores
        high_scores = ScoreManager.getInstance().load_high_scores() # get high scores
        for i, (username, score) in enumerate(high_scores):
            score_text = text_font.render(f"{i + 1}. {username}: {score}", True, WHITE)
            self.screen.blit(score_text, (self.screen.get_width() // 3, (self.screen.get_height() // 2) + i * 40))

        # Display Credits
        credits_text = small_text_font.render("Â© 2024 CPSC 6119 Team 4", True, WHITE)
        self.screen.blit(credits_text, (SCREEN_WIDTH // 2 - credits_text.get_width() // 2))


        # Waiting for player to press a key to start
        font = pygame.font.Font(None, 36) # set font size
        prompt = font.render("Press any key to start", True, WHITE)
        self.screen.blit(prompt, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2)) # draw onto screen
        pygame.display.flip() # update scrfeen contents

        # check if user pressed down on a key
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.state = "playing"
            elif event.type == pygame.QUIT:
                self.running = False

# game over state
    def game_over_screen(self):
        # display 'game over' screen
        self.screen.fill((0,0,0))
        font = pygame.font.Font(None, 74)
        message = font.render("Game Over", True, (255, 0, 0))
        self.screen.blit(message, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3)) # draw onto screen

        pygame.display.flip()
        pygame.time.wait(5000) # show 'game over' screen for 5 seconds
        self.running = False # end game

    def main_game(self):
        # Main game logic
        self.map.draw(self.screen) # draw the maze layout
        self.player.update() # update the movement of player
        self.player.draw(self.screen) # draw updated player based on movement

        for ghost in self.ghosts:
            ghost.update() # update movement
            ghost.draw(self.screen) # draw updated ghost based on movement
        
        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running == False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = "game_over"

    def run(self):
        while self.running:
            if self.state == "start_menu":
                self.start_menu()
            elif self.state == "playing":
                self.main_game()
            elif self.state == "game_over":
                self.game_over_screen()
            
            self.clock.tick(FPS) # setting fps to 60
        pygame.quit()

if __name__ == "__main__":
    game = GameEngine()
    game.run()