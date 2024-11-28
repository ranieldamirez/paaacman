from observer_pattern import Observer

class GameEventManager(Observer):
    def __init__(self, game_engine):
        self.game_engine = game_engine  # Reference to the GameEngine
        self.super_mode_timer = 0  # Frames left for super mode

    def update(self, event_type, data):
        """React to game events."""
        if event_type == "pellet_collected":
            self.handle_pellet_collected(data)
        elif event_type == "super_pellet_collected":
            self.handle_super_pellet_collected(data)
        elif event_type == "ghost_eaten":
            self.handle_ghost_eaten(data)
        elif event_type == "game_over":
            self.handle_game_over()

    def handle_pellet_collected(self, data):
        """Update score and check for level completion."""
        self.game_engine.score_manager.add_score(10)
        if self.game_engine.map.all_pellets_collected():
            print("Level complete!")
            self.game_engine.state = "game_over"

    def handle_super_pellet_collected(self, data):
        """Activate super mode and update score."""
        self.game_engine.score_manager.add_score(50)
        self.super_mode_timer = 300  # 300 frames of super mode
        print("Super mode activated!")

    def handle_ghost_eaten(self, data):
        """Update score for eating a ghost."""
        self.game_engine.score_manager.add_score(200)
        print("Ghost eaten!")

    def handle_game_over(self):
        """Trigger game-over state."""
        print("Game over!")
        self.game_engine.state = "game_over"

    def update_super_mode(self):
        """Decrement the super mode timer."""
        if self.super_mode_timer > 0:
            self.super_mode_timer -= 1
            if self.super_mode_timer == 0:
                print("Super mode ended!")
