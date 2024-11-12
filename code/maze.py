# maze.py
import pygame

class Maze:
    def __init__(self):
        self.walls = [
            pygame.Rect(100, 100, 200, 10),  # Add maze walls here
            pygame.Rect(400, 300, 10, 200),
        ]

    def draw(self, screen):
        for wall in self.walls:
            pygame.draw.rect(screen, (0, 0, 255), wall)  # Blue walls
