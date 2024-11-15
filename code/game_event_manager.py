# game_event_manager.py
import pygame

class GameEventManager:
    def check_collision(self, player, ghosts):
        for ghost in ghosts:
            if player.rect.colliderect(ghost.rect):
                return True
        return False
