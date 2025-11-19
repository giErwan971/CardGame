import pygame

screen_info = None
resoCible = None
resolution = None
offsets = None

def init():
    global screen_info, resoCible, resolution, offsets
    screen_info = pygame.display.Info()
    resoCible = [315, 250]
    resolution = [screen_info.current_w, screen_info.current_h]
    offsets = [0, 0]
    ratio = resolution[0] / resolution[1]
    if ratio > resoCible[0] / resoCible[1]:
        lastW = resolution[0]
        resolution[0] = resolution[1] / resoCible[1] * resoCible[0]
        offsets[0] = (lastW - resolution[0]) / 2
    elif ratio > resoCible[1] / resoCible[0]:
        lastH = resolution[1]
        resolution[1] = resolution[0] / resoCible[0] * resoCible[1]
        offsets[1] = lastH - resolution[1] / 2



def getScaledMousePosUI():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    scale_x = resoCible[0] / resolution[0]
    scale_y = resoCible[1] / resolution[1]
    return ((mouse_x - offsets[0]) * scale_x, (mouse_y - offsets[1]) * scale_y)


def getScaledMousePosCards():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    scale_x = resoCible[0] * 2 / resolution[0]
    scale_y = resoCible[1] * 2 / resolution[1]
    return (
        int((mouse_x - offsets[0]) * scale_x),
        int((mouse_y - offsets[1]) * scale_y),
    )