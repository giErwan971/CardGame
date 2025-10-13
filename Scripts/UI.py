import pygame
class Button:
    def __init__(self, rect: pygame.Rect, text, bg, function):
        self.rect = rect
        self.text = text
        self.bg = pygame.image.load(bg)
        self.function = function

    def show(self, screen : pygame.Surface):
        screen.blit(self.bg, (self.rect.x, self.rect.y))
    
    def isClic(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.function()
    