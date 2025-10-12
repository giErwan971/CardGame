import pygame
from win32api import GetSystemMetrics


        #   ----- ADAPTER RESOLUTION ----  #
resolution = [GetSystemMetrics (0), GetSystemMetrics (1)]
offsets = [0, 0]
ratio = resolution[0] / resolution[1]
if ratio > 4/3:
    lastW = resolution[0]
    resolution[0] = resolution[1] / 3 * 4
    offsets[0] = (lastW-resolution[0])/2
elif ratio > 4/3:
    lastH = resolution[1]
    resolution[1] = resolution[0] / 4 * 3
    offsets[1] = (lastH - resolution[1]/2)


        #   --- INITIALISATION PYGAME ---  #
pygame.init()
ecran = pygame.display.set_mode((GetSystemMetrics (0), GetSystemMetrics (1)), pygame.FULLSCREEN)
pygame.draw.rect(ecran, (180, 20, 150), (offsets[0], offsets[1], resolution[0], resolution[1]))
pygame.display.flip()


        #   ------- BOUCLE DE JEU -------  #
run = True
while run:
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
            run = False

pygame.quit()