import pygame
class Button:
    def __init__(self, rect: pygame.Rect, imgOffsets, text, bg: pygame.Surface, function):
        self.rect = rect
        self.imgOffets = imgOffsets
        self.text = text
        self.bg = bg
        self.function = function
        mouseIn = False

    def setImage(self, bg: pygame.Surface):
        self.bg = bg

    def show(self, screen : pygame.Surface):
        screen.blit(self.bg, (self.rect.x - self.imgOffets[0], self.rect.y - self.imgOffets[1]))
    
    def isClic(self, resoCible, resolution, offsets):
        if self.rect.collidepoint(get_scaled_mouse_pos(resoCible, resolution, offsets)):
            self.function()

    def MouseEnter(self):
        if mouseIn == False and self.rect.collidepoint(pygame.mouse.get_pos()):
            mouseIn = True
            return True
        return False
    
    def MouseExit(self):
        if mouseIn == True and not self.rect.collidepoint(pygame.mouse.get_pos()):
            mouseIn = False
            return True
        return False
    
def get_scaled_mouse_pos(resoCible, resolution, offsets):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    # Convertir les coordonnées de la souris de l'écran vers la surface redimensionnée
    scale_x = resoCible[0] / resolution[0]
    scale_y = resoCible[1] / resolution[1]
    return (
        (mouse_x - offsets[0]) * scale_x,
        (mouse_y - offsets[1]) * scale_y
    )
    