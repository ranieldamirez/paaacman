from observer_pattern import Observer
from MovementStrategy import *

class GameEventManager(Observer):
    def __init__(self, game_engine):
        self.game_engine = game_engine  # Reference to the GameEngine
        self.super_mode_timer = 0  # Frames left for super mode
        self.player_lives = 3 # Player has 3 lives
        self.current_level = 1  # Start at level 1
        self.max_level = 10  # Maximum number of levels

    def update(self, event_type, data):
        """React to game events."""
        if event_type == "pellet_collected":
            self.handle_pellet_collected(data)
        elif event_type == "super_pellet_collected":
            self.handle_super_pellet_collected(data)
        elif event_type == "ghost_eaten":
            self.handle_ghost_eaten(data)
        elif event_type == "player_collided_with_ghost":
            self.handle_player_collision(data)

    def handle_pellet_collected(self, data):
        """Update score and check for level completion."""
        self.game_engine.score_manager.add_score(10)
        if self.game_engine.map.all_pellets_collected():
            if self.current_level < self.max_level:
                self.current_level += 1
                self.game_engine.state = "level_complete"
            else:
                self.game_engine.state = "game_over"
    
    def draw_level_display(self, screen, font):
        """Draw the current level on the GUI."""
        level_text = font.render(f"Level: {self.current_level}", True, (255, 255, 255))
        screen.blit(level_text, (800 - 150, 10))
        
    def handle_super_pellet_collected(self, data):
        """Activate super mode and update score."""
        self.game_engine.score_manager.add_score(50)
        self.super_mode_timer = 300  # 300 frames of super mode
        
        # Change ghosts to look scared
        for ghost in self.game_engine.ghosts:
            ghost.set_scared()
            ghost.set_strategy(ScaredMovement()) # Change to scared movements

    def handle_player_collision(self, data):
        """Handle collision between the player and a ghost."""
        self.player_lives -= 1
        
        if self.player_lives > 0:
            self.game_engine.reset_player_and_ghosts()  # Reset player position
        else:
            self.game_engine.state = "game_over"


    def handle_ghost_eaten(self, data):
        """Update score for eating a ghost."""
        self.game_engine.score_manager.add_score(200)

    def update_super_mode(self):
        """Decrement the super mode timer."""
        if self.super_mode_timer > 0:
            self.super_mode_timer -= 1
            if self.super_mode_timer == 0:

                # Reset all ghosts to their original appearance
                for ghost in self.game_engine.ghosts:
                    ghost.reset_appearance()
                    ghost.set_strategy(ChaseMovement())
