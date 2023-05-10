import pygame

class HealthBar:
    def __init__(self, x, y, width = 40, height = 3, max_health=100, color=(255, 0, 0), background_color=(0, 0, 0), border_color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_health = max_health
        self.current_health = max_health
        self.color = color
        self.background_color = background_color
        self.border_color = border_color

    def update(self, current_health):
        self.current_health = current_health

    def draw(self, screen):
        # Draw the background
        pygame.draw.rect(screen, self.background_color, (self.x, self.y, self.width, self.height))

        # Calculate the health bar width
        health_bar_width = int((self.current_health / self.max_health) * self.width)

        # Draw the health bar
        pygame.draw.rect(screen, self.color, (self.x, self.y, health_bar_width, self.height))

        # Draw the border
        pygame.draw.rect(screen, self.border_color, (self.x, self.y, self.width, self.height), 1)
