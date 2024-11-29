import pygame
from player import Player
from enemy import Enemy
from maze import Maze
from score_manager import ScoreManager
from game_event_manager import GameEventManager
from SuperPlayerDecorator import SuperPlayerDecorator
from MovementStrategy import RandomMovement, ChaseMovement
import sys

# Screen configuration
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
cell_size = 25
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

# Fonts
pygame.init()
title_font = pygame.font.Font(None, 100)
text_font = pygame.font.Font(None, 36)

# Load the PAAAC-MAN image
try:
    paaacman_image = pygame.image.load("./resources/PAAAC.jpg")
    paaacman_image = pygame.transform.scale(paaacman_image, (100, 100))
except pygame.error:
    print("ERROR: Unable to load the image.")
    sys.exit()

class GameEngine:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("PAAAC-MAN Arcade Game")
        self.clock = pygame.time.Clock()
        self.lives_display = pygame.Surface((30,30))
        self.lives_display.fill((255, 255, 0))


        # Initialize game elements
        self.map = Maze(SCREEN_WIDTH, SCREEN_HEIGHT, cell_size)
        self.player = Player(cell_size, self.map)
        self.ghosts = [Enemy(cell_size, self.map, strategy=ChaseMovement()) for _ in range(4)]
        self.score_manager = ScoreManager()
        self.event_manager = GameEventManager(self)
        self.game_over_timer = None

        self.running = True
        self.state = "start_menu"
        self.frame_count = 0

        # Place 2 ghosts in jail
        self.ghosts[2].remove(self.map)
        self.ghosts[3].remove(self.map)

        # Register observers
        self.player.add_observer(self.event_manager)
        for ghost in self.ghosts:
            ghost.add_observer(self.event_manager)

    def start_menu(self, events):
        """Render the start menu."""
        self.screen.fill(BLACK)
        title_text = title_font.render("PAAAC-MAN", True, YELLOW)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        self.screen.blit(title_text, title_rect)

        # Display image
        self.screen.blit(paaacman_image, (SCREEN_WIDTH // 2 - paaacman_image.get_width() // 2, SCREEN_HEIGHT // 2))

        # Start prompt
        prompt = text_font.render("Press any key to start", True, WHITE)
        self.screen.blit(prompt, (SCREEN_WIDTH // 3, SCREEN_HEIGHT - 100))

        pygame.display.flip()

        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.state = "playing"

    def pause_menu(self, events):
        """Render the pause menu."""
        self.screen.fill(BLACK)
        pause_text = title_font.render("Paused", True, YELLOW)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        self.screen.blit(pause_text, pause_rect)

        resume_prompt = text_font.render("Press R to Resume", True, WHITE)
        quit_prompt = text_font.render("Press Q to Quit", True, WHITE)
        self.screen.blit(resume_prompt, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2))
        self.screen.blit(quit_prompt, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2 + 50))

        pygame.display.flip()

        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.state = "playing"
                elif event.key == pygame.K_q:
                    self.running = False
    def reset_player_and_ghosts(self):
        self.player.rect.topleft = (self.map.cell_size, self.map.cell_size)  # Reset player position
        self.ghosts[1].remove(self.map)  # Send ghosts back to jail
        self.ghosts[0].remove(self.map)
        print("Player and ghosts reset after losing a life.")

    def draw_lives(self):
        """Draw lives on screen."""
        for i in range(self.event_manager.player_lives):
            self.screen.blit(self.lives_display, (10 + i * 35, SCREEN_HEIGHT - 40))
    def main_game(self, events):
        """Main game loop."""
        self.frame_count += 1

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.state = "paused"

        self.screen.fill(BLACK)

        # Pellet collection
        new_player = self.player.collect_pellet(self.map)
        if isinstance(new_player, SuperPlayerDecorator):
            self.player = new_player

        # Update the player
        updated_player = self.player.update(self.map, self.ghosts)
        if updated_player != self.player:
            self.player = updated_player

        # Update super mode timer
        self.event_manager.update_super_mode()

        # Draw maze, player, and ghosts
        self.map.draw(self.screen)
        self.player.draw(self.screen)
        for ghost in self.ghosts:
            ghost.update(self.map, self.player)
            ghost.draw(self.screen)

        # Game over conditions
        if isinstance(self.player, Player) and self.player.collides_with_ghost(self.ghosts):
            return
        elif self.map.all_pellets_collected():
            self.state = "game_over"

        self.draw_lives()

        # Display score
        score_text = text_font.render(f"Score: {self.score_manager.get_current_score()}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        pygame.display.flip()

        
        

    def game_over_screen(self):
        """Render game over screen."""
        self.screen.fill(BLACK)
        game_over_text = title_font.render("Game Over", True, YELLOW)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        self.screen.blit(game_over_text, game_over_rect)

        prompt = text_font.render("Exiting game in 3 seconds...", True, WHITE)
        prompt_rect = prompt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(prompt, prompt_rect)

        pygame.display.flip()

        current_time = pygame.time.get_ticks()
        if self.game_over_timer is None:
            self.game_over_timer = current_time

        if current_time - self.game_over_timer >= 3000:
            pygame.quit()
            sys.exit()

    def run(self):
        """Run the game loop."""
        while self.running:
            events = pygame.event.get()
            if self.state == "start_menu":
                self.start_menu(events)
            elif self.state == "playing":
                self.main_game(events)
            elif self.state == "paused":
                self.pause_menu(events)
            elif self.state == "game_over":
                self.game_over_screen()

            self.clock.tick(FPS)

        pygame.quit()


if __name__ == "__main__":
    game = GameEngine()
    game.run()
