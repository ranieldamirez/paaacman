 # enemy.py
import pygame
import random

class Enemy:
    def __init__(self):
        self.position = [random.randint(100, 700), random.randint(100, 500)]
        self.image = pygame.Surface((20, 20))  # Placeholder
        self.image.fill((255, 0, 0))  # Red color
        self.rect = self.image.get_rect(topleft=self.position)
        self.speed = 3

    def update(self):
        self.rect.x += random.choice([-self.speed, self.speed])
        self.rect.y += random.choice([-self.speed, self.speed])

    def draw(self, screen):
        screen.blit(self.image, self.rect)
