# player.py
import pygame

class Player:
    def __init__(self):
        self.position = [50, 50]  # Start position
        self.image = pygame.Surface((20, 20))  # Placeholder
        self.image.fill((255, 255, 0))  # Yellow color
        self.rect = self.image.get_rect(topleft=self.position)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)
