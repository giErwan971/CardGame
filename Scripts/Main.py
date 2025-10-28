import pygame
import UI
import Cards
from win32api import GetSystemMetrics
import time
#numpy est neccessaire pour la fonction bloomCombination mais pas besion d'import

        #   ------- FONCTION CLEE -------  #
def getScaledMousePosUI():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    scale_x = resoCible[0] / resolution[0]
    scale_y = resoCible[1] / resolution[1]
    return (
        (mouse_x - offsets[0]) * scale_x,
        (mouse_y - offsets[1]) * scale_y
    )

def getScaledMousePosCards():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    scale_x = resoCible[0] * 2 / resolution[0]
    scale_y = resoCible[1] * 2 / resolution[1]
    return (
        int((mouse_x - offsets[0]) * scale_x),
        int((mouse_y - offsets[1]) * scale_y)
    )

def bloomCombination(combinationNumber: int):
    combination = deck.onTable[combinationNumber]
    rect = pygame.Rect(31*2+(combinationNumber%11)*42, 52*2+combinationNumber//11*(15*len(onTable[combinationNumber-11])+55), 36, 15*len(combination)+37)
    if rect.collidepoint(getScaledMousePosCards()):
        bloomSurface = pygame.Surface((rect.width+10, rect.height+10), pygame.SRCALPHA)
        rect = pygame.Rect(31*2+(combinationNumber%11)*42, 52*2+combinationNumber//11*(15*len(onTable[combinationNumber-11])+55), 36, (15*len(combination)+37)/2)
        for y in range(bloomSurface.get_height()):
            alpha = int(150 * (1 - y / bloomSurface.get_height()))
            if not rect.collidepoint(getScaledMousePosCards()) and alpha != 0:
                alpha = 150 - alpha
            pygame.draw.line(bloomSurface, (0, 150, 255, alpha), (0, y), (bloomSurface.get_width(), y))
        # Ajouter l'arrondi des coins
        surf_array = pygame.surfarray.pixels_alpha(bloomSurface)
        for x in range(8):
            for y in range(8):
                if (x-8)**2 + (y-8)**2 > 64:  # rayon de 8 pixels
                    surf_array[x,y] = 0  # coin supérieur gauche
                    surf_array[bloomSurface.get_width()-1-x,y] = 0  # coin supérieur droit
                    surf_array[x,bloomSurface.get_height()-1-y] = 0  # coin inférieur gauche
                    surf_array[bloomSurface.get_width()-1-x,bloomSurface.get_height()-1-y] = 0  # coin inférieur droit
        del surf_array  # libérer la surface
        CardsScreen.blit(bloomSurface, (rect.x-5, rect.y-5))

def dropCardOnTable(card: Cards.Card, combinationNumber: int):
    combination = deck.onTable[combinationNumber]
    rect = pygame.Rect(31*2+(combinationNumber%11)*42, 52*2+combinationNumber//11*(15*len(onTable[combinationNumber-11])+55), 36, 15*len(combination)+37)
    if rect.collidepoint(getScaledMousePosCards()) and selectedCard != None:
        rect = pygame.Rect(31*2+(combinationNumber%11)*42, 52*2+combinationNumber//11*(15*len(onTable[combinationNumber-11])+55), 36, (15*len(combination)+37)/2)
        if rect.collidepoint(getScaledMousePosCards()):
            deck.playCard(card, True)
            combination.insert(0, card)
            onTable[combinationNumber] = combination
        else:
            deck.playCard(card, True)
            combination.append(card)
            onTable[combinationNumber] = combination

def cardToMouse(card: Cards.Card):
    card.show(CardsScreen, (getScaledMousePosCards()[0]-18, getScaledMousePosCards()[1]-26))

def isCorectCombination(combination: list[Cards.Card]) -> bool:
    isCorect = False
    #LES CARRES
    if len(combination) == 4 or len(combination) == 3:
        same_value = all(card.value == combination[0].value for card in combination)
        different_colors = len(set(card.color for card in combination)) == len(combination)
        isCorect = same_value and different_colors
    #LES SUITES
    if all(card.color == combination[0].color for card in combination):
        combination.sort(key=lambda card: card.value)
        index = combination[0].value
        isCorect = True
        for card in combination:
            if card.value != index:
                isCorect = False
                break
            index += 1
        if combination[0].value == 1 and not isCorect:
            combination[0].value = 14
            combination.sort(key=lambda card: card.value)
            index = combination[0].value
            isCorect = True
            for card in combination:
                if card.value != index:
                    isCorect = False
                    break
                index += 1
    return isCorect

def checkCombinations(allCombinations: list[list[Cards.Card]]) -> tuple:
    for i in range(len(allCombinations)):
        combination = allCombinations[i]
        if len(combination) >= 3:
            while len(combination) >= 6:
                allCombinations.insert(i+1, combination[len(combination)-3:len(combination)])
                combination = combination[0:len(combination)-3]
                allCombinations[i] = combination
            if not isCorectCombination(combination):
                return (False, [card.value for card in combination])
        else:
            return (False, [card.value for card in combination])
    return (True, allCombinations)

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
UIScreen = pygame.Surface((resoCible[0], resoCible[1]))
CardsScreen = pygame.Surface((resolution[0], resolution[1]), pygame.SRCALPHA)

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

cardsBox = pygame.image.load('Assets\\MainMenu\\CardsBox.png')
cardsDeck = pygame.image.load('Assets\\MainMenu\\CardsDeck.png')
drawPileAssets = pygame.image.load("Assets\\Cards\\King's Cards\\Back And Joker\\DrawPile.png")
backCard = pygame.image.load("Assets\\Cards\\King's Cards\\Back And Joker\\Back_1.png")



        #   ------ LES ANNIMATIONS ------  #
annimationPlayButton_actuelFrame = 0
annimationPlayButton_isMouseOn = False
def annimationPlayButton():
    global annimationPlayButton_actuelFrame, annimationPlayButton_isMouseOn
    actuelFrame = annimationPlayButton_actuelFrame
    isMouseOn = playButton.rect.collidepoint(getScaledMousePosUI())
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
    isMouseOn = teamButton.rect.collidepoint(getScaledMousePosUI())
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
    isMouseOn = jeton1rect.collidepoint(getScaledMousePosUI())
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
    isMouseOn = jeton2rect.collidepoint(getScaledMousePosUI())
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
    global UIScreen, resoCible, resolution, isOnMainMenu
    isOnMainMenu = False
    UIScreen = pygame.transform.scale(UIScreen, (resoCible[0], resoCible[1]))
    pygame.draw.rect(UIScreen, (255,255,255), pygame.Rect(0, 0, resoCible[0], resoCible[1]))
    UIScreen = pygame.transform.scale(UIScreen, (resolution[0], resolution[1]))
    teamButton.isActive = False
    playButton.isActive = False

def teamButtonClic():
    print("Team Pressed")

#LES BOUTONS
playButton = UI.Button(pygame.Rect(125, 65, 64, 48), (11, 0), "PlayButton", playButtonTiles[0], playButtonClic)
teamButton = UI.Button(pygame.Rect(125, 144, 64, 48), (11, 0), "TeamButton", teamButtonTiles[0], teamButtonClic)
allButton = [playButton, teamButton]

        #   ------- BOUCLE DE JEU -------  #
deck = Cards.Deck()
deck.shuffleDeck()
for i in range(1):
    cardTest = deck.pickCard()
    deck.inHand.append(cardTest)
for i in range(1):
    cardTest = deck.pickCard()
    deck.inOpponentHand.append(cardTest)
tmp = []
for j in range(4):
    cardTest = deck.pickCard()
    tmp.append(cardTest)
deck.onTable.append(tmp)
for i in range(12):
    tmp = []
    for j in range(6):
        cardTest = deck.pickCard()
        tmp.append(cardTest)
    deck.onTable.append(tmp)
selectedCard = None
run = True
isOnMainMenu = True
while run:
    drawPile = deck.drawPile
    onTable = deck.onTable
    inHand = deck.inHand
    inOpponentHand = deck.inOpponentHand
    #LES EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in allButton:
                button.isClic(resoCible, resolution, offsets)
            for i in range(len(inHand)):
                if pygame.Rect(13*2+i*44+(13-len(inHand))*22, 215*2, 37, 52).collidepoint(getScaledMousePosCards()):
                    selectedCard = inHand[i]
        if event.type == pygame.MOUSEBUTTONUP:
            for i in range(len(onTable)):
                dropCardOnTable(selectedCard, i)
            selectedCard = None

    #LES GRAPHISMES
    UIScreen = pygame.transform.scale(UIScreen, (resoCible[0], resoCible[1]))
    CardsScreen = pygame.transform.scale(CardsScreen, (resoCible[0]*2, resoCible[1]*2))
    UIScreen.fill((0, 0, 0))
    CardsScreen.fill((0, 0, 0, 0))

    if isOnMainMenu:
        UIScreen.blit(backgroundMain, (0, 0))
        UIScreen.blit(cardsBox, (35, 126))
        UIScreen.blit(cardsDeck, (231, 127))
        UIScreen.blit(jeton2, (jeton2rect.x, jeton2rect.y))
        UIScreen.blit(jeton1, (jeton1rect.x, jeton1rect.y))
        playButton.show(UIScreen)
        teamButton.show(UIScreen)
        
        annimationTeamButton()
        annimationPlayButton()
        annimationJeton1()
        annimationJeton2()

    else:
        UIScreen.blit(backgroundMain, (0, 0))
        UIScreen.blit(drawPileAssets, (268, 99))

        #Les cartes sur la table
        for x in range(len(onTable)):
            if selectedCard != None:
                bloomCombination(x)
            for y in range(len(onTable[x])):
                onTable[x][y].show(CardsScreen, (31*2+(x%11)*42, 52*2+y*15+x//11*(15*len(onTable[x-11])+55)))

        #les cartes en main
        for i in range(len(inHand)):
            if selectedCard != inHand[i]:
                if pygame.Rect(13*2+i*44+(13-len(inHand))*22, 215*2, 37, 52).collidepoint(getScaledMousePosCards()):
                    inHand[i].show(CardsScreen, (13*2+i*44+(13-len(inHand))*22, 210*2), True)
                else:
                    inHand[i].show(CardsScreen, (13*2+i*44+(13-len(inHand))*22, 215*2))
            else:
                cardToMouse(inHand[i])
        for i in range(len(inOpponentHand)):
            CardsScreen.blit(backCard, (90*2+i*32+(13-len(inOpponentHand))*22, 4*2+i*3))
        

    UIScreen = pygame.transform.scale(UIScreen, (resolution[0], resolution[1]))
    CardsScreen = pygame.transform.scale(CardsScreen, (resolution[0], resolution[1]))
    UIScreen.blit(CardsScreen, (0, 0))

    screen.blit(UIScreen, (offsets[0], offsets[1]))

    pygame.display.flip()
    time.sleep(0.01)

pygame.quit()