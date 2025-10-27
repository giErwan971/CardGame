import pygame
import UI
from win32api import GetSystemMetrics
import time

        #   ------- FONCTION CLEE -------  #
def get_scaled_mouse_pos():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    # Convertir les coordonnées de la souris de l'écran vers la surface redimensionnée
    scale_x = resoCible[0] / resolution[0]
    scale_y = resoCible[1] / resolution[1]
    return (
        (mouse_x - offsets[0]) * scale_x,
        (mouse_y - offsets[1]) * scale_y
    )

        #   --- INITIALISATION PYGAME ---  #
pygame.init()
screen = pygame.display.set_mode((GetSystemMetrics (0), GetSystemMetrics (1)), pygame.FULLSCREEN)


        #   ----- ADAPTER RESOLUTION ----  #
resoCible = [315, 250]
resolution = [GetSystemMetrics (0), GetSystemMetrics (1)]
offsets = [0, 0]
ratio = resolution[0] / resolution[1]
if ratio > resoCible[0] / resoCible[1]:
    lastW = resolution[0]
    resolution[0] = resolution[1] / resoCible[1] * resoCible[0]
    offsets[0] = (lastW-resolution[0])/2
elif ratio > resoCible[1] / resoCible[0]:
    lastH = resolution[1]
    resolution[1] = resolution[0] / resoCible[0] * resoCible[1]
    offsets[1] = (lastH - resolution[1]/2)
resizeScreen = pygame.Surface((resoCible[0], resoCible[1]))

        #   --------- LES IMAGES --------  #
backgroundMain = pygame.image.load('Assets\\MainMenu\\BackGround.png')
backgroundMain = backgroundMain.convert()

jeton2TileMap = pygame.image.load('Assets\\MainMenu\\Jeton\\jeton2TileMap.png')
jeton2Tiles = [jeton2TileMap.subsurface(x,0,64,72)for x in range(0,256,64)]
jeton2rect = pygame.Rect(196, 49, 64, 72)
jeton2 = jeton2Tiles[0]

jeton1TileMap = pygame.image.load('Assets\\MainMenu\\Jeton\\jeton1TileMap.png')
jeton1Tiles = [jeton1TileMap.subsurface(x,0,69,61)for x in range(0,552,69)]
jeton1rect = pygame.Rect(41, 58, 69, 61)
jeton1 = jeton1Tiles[0]

playButtonTileMap = pygame.image.load('Assets\\MainMenu\\Button\\PlayTileMap.png')
playButtonTiles = [playButtonTileMap.subsurface(x,0,86,48)for x in range(0,774,86)]
teamButtonTileMap = pygame.image.load('Assets\\MainMenu\\Button\\TeamTileMap.png')
teamButtonTiles = [teamButtonTileMap.subsurface(x,0,86,48)for x in range(0,774,86)]

        #   ------ LES ANNIMATIONS ------  #
annimationPlayButton_actuelFrame = 0
annimationPlayButton_isMouseOn = False
def annimationPlayButton():
    global annimationPlayButton_actuelFrame, annimationPlayButton_isMouseOn
    actuelFrame = annimationPlayButton_actuelFrame
    isMouseOn = playButton.rect.collidepoint(get_scaled_mouse_pos())
    if isMouseOn and actuelFrame < len(playButtonTiles)-1:
        actuelFrame += 1
        playButton.setImage(playButtonTiles[actuelFrame])
    elif not isMouseOn and actuelFrame > 0:
        actuelFrame -= 1
        playButton.setImage(playButtonTiles[actuelFrame])
    annimationPlayButton_isMouseOn = isMouseOn
    annimationPlayButton_actuelFrame = actuelFrame


annimationTeamButton_actuelFrame = 0
annimationTeamButton_isMouseOn = False
def annimationTeamButton():
    global annimationTeamButton_actuelFrame, annimationTeamButton_isMouseOn
    actuelFrame = annimationTeamButton_actuelFrame
    isMouseOn = teamButton.rect.collidepoint(get_scaled_mouse_pos())
    if isMouseOn and actuelFrame < len(teamButtonTiles)-1:
        actuelFrame += 1
        teamButton.setImage(teamButtonTiles[actuelFrame])
    elif not isMouseOn and actuelFrame > 0:
        actuelFrame -= 1
        teamButton.setImage(teamButtonTiles[actuelFrame])
    annimationTeamButton_isMouseOn = isMouseOn
    annimationTeamButton_actuelFrame = actuelFrame

annimationJeton1_actuelFrame = 0
annimationJeton1_isMouseOn = False
def annimationJeton1():
    global annimationJeton1_actuelFrame, annimationJeton1_isMouseOn, jeton1
    actuelFrame = annimationJeton1_actuelFrame
    isMouseOn = jeton1rect.collidepoint(get_scaled_mouse_pos())
    if isMouseOn and actuelFrame < len(jeton1Tiles)-1:
        actuelFrame += 1
        jeton1 = jeton1Tiles[actuelFrame]
    elif not isMouseOn and actuelFrame > 0:
        actuelFrame -= 1
        jeton1 = jeton1Tiles[actuelFrame]
    annimationJeton1_isMouseOn = isMouseOn
    annimationJeton1_actuelFrame = actuelFrame


annimationJeton2_actuelFrame = 0
annimationJeton2_isMouseOn = False
def annimationJeton2():
    global annimationJeton2_actuelFrame, annimationJeton2_isMouseOn, jeton2
    actuelFrame = annimationJeton2_actuelFrame
    isMouseOn = jeton2rect.collidepoint(get_scaled_mouse_pos())
    if isMouseOn and actuelFrame < len(jeton2Tiles)-1:
        actuelFrame += 1
        jeton2 = jeton2Tiles[actuelFrame]
    elif not isMouseOn and actuelFrame > 0:
        actuelFrame -= 1
        jeton2 = jeton2Tiles[actuelFrame]
    annimationJeton2_isMouseOn = isMouseOn
    annimationJeton2_actuelFrame = actuelFrame

        #   --------- LES BOUTONS --------  #
#LEURS FONCTIONS
def playButtonClic():
    global resizeScreen, resoCible, resolution, isOnMainMenu
    isOnMainMenu = False
    resizeScreen = pygame.transform.scale(resizeScreen, (resoCible[0], resoCible[1]))
    pygame.draw.rect(resizeScreen, (255,255,255), pygame.Rect(0, 0, resoCible[0], resoCible[1]))
    resizeScreen = pygame.transform.scale(resizeScreen, (resolution[0], resolution[1]))

def teamButtonClic():
    print("Team Pressed")

#LES BOUTONS
playButton = UI.Button(pygame.Rect(125, 65, 64, 48), (11, 0), "PlayButton", playButtonTiles[0], playButtonClic)
teamButton = UI.Button(pygame.Rect(125, 144, 64, 48), (11, 0), "TeamButton", teamButtonTiles[0], teamButtonClic)
allButton = [playButton, teamButton]

        #   ------- BOUCLE DE JEU -------  #
run = True
isOnMainMenu = True
while run:
    #LES EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in allButton:
                button.isClic(resoCible, resolution, offsets)

    #LES GRAPHISMES
    resizeScreen = pygame.transform.scale(resizeScreen, (resoCible[0], resoCible[1]))

    if isOnMainMenu:
        resizeScreen.blit(backgroundMain, (0, 0))
        resizeScreen.blit(jeton2, (jeton2rect.x, jeton2rect.y))
        resizeScreen.blit(jeton1, (jeton1rect.x, jeton1rect.y))
        playButton.show(resizeScreen)
        teamButton.show(resizeScreen)
        
        annimationTeamButton()
        annimationPlayButton()
        annimationJeton1()
        annimationJeton2()
    else:
        pass
    resizeScreen = pygame.transform.scale(resizeScreen, (resolution[0], resolution[1]))
    screen.blit(resizeScreen, (offsets[0], offsets[1]))
    pygame.display.flip()
    time.sleep(0.01)

pygame.quit()