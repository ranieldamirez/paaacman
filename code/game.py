import pygame
from player import Player
from enemy import Enemy
from maze import Maze
from score_manager import ScoreManager
from game_event_manager import GameEventManager
from SuperPlayerDecorator import SuperPlayerDecorator
import sys

pygame.init()

# Screen configuration
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
cell_size = 25
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

# Fonts
title_font = pygame.font.Font(None, 100)
text_font = pygame.font.Font(None, 36)

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

        # Initialize game elements
        self.map = Maze(SCREEN_WIDTH, SCREEN_HEIGHT, cell_size)
        self.player = Player(cell_size, self.map)
        self.ghosts = [Enemy(cell_size, self.map) for _ in range(4)]
        self.score_manager = ScoreManager()
        self.event_manager = GameEventManager()

        self.running = True
        self.state = "start_menu"  # Game starts at the menu
        self.frame_count = 0  # Frame counter for timed events

        # Place 2 ghosts in jail
        self.ghosts[2].remove(self.map)
        self.ghosts[3].remove(self.map)

    def start_menu(self, events):
        """Render the start menu."""
        self.screen.fill(BLACK)
        title_text = title_font.render("PAAC-MAN", True, YELLOW)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        self.screen.blit(title_text, title_rect)

        # Display image next to the title
        self.screen.blit(paaacman_image, (SCREEN_WIDTH // 2 - paaacman_image.get_width() // 2, SCREEN_HEIGHT // 2))

        # Display start prompt
        prompt = text_font.render("Press any key to start", True, WHITE)
        self.screen.blit(prompt, (SCREEN_WIDTH // 3, SCREEN_HEIGHT - 100))

        pygame.display.flip()

        # Check events to transition to the game
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.state = "playing"

    def main_game(self, events):
        """Main game loop for handling gameplay."""
        self.frame_count += 1  # Increment the frame count

        

        # Clear the screen
        self.screen.fill(BLACK)

        # Handle pellet collection
        new_player = self.player.collect_pellet(self.map)
        if isinstance(new_player, SuperPlayerDecorator):
            self.player = new_player  # Replace player if power-up is active
        else:
            self.player = self.player.update(self.map, self.ghosts)

        # Draw maze, player, and ghosts
        self.map.draw(self.screen)
        self.player.draw(self.screen)

        # Manage ghost spawning
        print(self.frame_count)

        for ghost in self.ghosts:
            ghost.update(self.map, self.player)
            ghost.draw(self.screen)

        # Display the score
        score_text = text_font.render(f"Score: {self.score_manager.getInstance().get_current_score()}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        # Update the display
        pygame.display.flip()

        # Check for game over conditions
        if isinstance(self.player, Player) and self.player.collides_with_ghost(self.ghosts):
            self.state = "game_over"
        elif self.map.all_pellets_collected():
            self.state = "game_over"

    def game_over_screen(self):
        """Render the game over screen."""
        self.screen.fill(BLACK)
        game_over_text = title_font.render("Game Over", True, YELLOW)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        self.screen.blit(game_over_text, game_over_rect)

        # Display restart or exit prompt
        prompt = text_font.render("Press any key to restart or ESC to exit", True, WHITE)
        prompt_rect = prompt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(prompt, prompt_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                else:
                    self.state = "start_menu"

    def run(self):
        """Run the game loop."""
        while self.running:
            events = pygame.event.get()  # Get all events at the start of the frame

            # Handle quitting the game with ESC globally
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False

            if self.state == "start_menu":
                self.start_menu(events)
            elif self.state == "playing":
                self.main_game(events)
            elif self.state == "game_over":
                self.game_over_screen()

            self.clock.tick(FPS)  # Limit the frame rate

        pygame.quit()


if __name__ == "__main__":
    game = GameEngine()
    game.run()
