import pygame

screen_info = None
resoCible = None
resolution = None
offsets = None

def init(resoCibleParam, resolutionParam, offsetsParam):
    global screen_info, resoCible, resolution, offsets
    screen_info = pygame.display.Info()
    resoCible = resoCibleParam
    resolution = resolutionParam
    offsets = offsetsParam



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