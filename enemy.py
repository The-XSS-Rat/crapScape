import pygame

# Add the following constant
ENEMY_SPEED = 2

# Add the following class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((16, 16))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = 100
        self.max_health = 100
        self.attack_damage = 10
        self.attack_cooldown = 100
        self.attack_timer = 0
        # Add the following lines to the Player class
        self.health = 100
        self.max_health = 100
        self.attack_damage = 10
        self.attack_cooldown = 100
        self.attack_timer = 0

    def attack(self, enemies):
        for enemy in enemies:
            if self.distance_to(enemy) < 32:
                enemy.health -= self.attack_damage
                if enemy.health <= 0:
                    enemy.kill()

    def update(self, player):
        dx, dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        distance = math.sqrt(dx * dx + dy * dy)
        if distance < 100:
            self.rect.x += ENEMY_SPEED * dx / distance
            self.rect.y += ENEMY_SPEED * dy / distance

            if self.attack_timer <= 0:
                self.attack_timer = self.attack_cooldown
                player.health -= self.attack_damage
                if player.health <= 0:
                    player.kill()
        self.attack_timer -= 1