import pygame

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, text, text_color, bg_color):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(bg_color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.text = text
        self.font = pygame.font.Font(None, 24)
        self.text_surf = self.font.render(self.text, True, text_color)
        W = self.text_surf.get_width()
        H = self.text_surf.get_height()
        self.image.blit(self.text_surf, ((width - W) // 2, (height - H) // 2))

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            return self.rect.collidepoint(mouse_pos)
        return False
