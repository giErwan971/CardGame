import pygame
import UI
import Cards
from win32api import GetSystemMetrics
import time
# numpy est neccessaire pour la fonction bloomCombination mais pas besion d'import


#   ------- FONCTION CLEE -------  #
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


def bloomCombination(combinationNumber: int):
    global onTable
    combination = onTable[combinationNumber]
    x = combinationNumber
    row = x // 11
    if row == 0:
        rect = pygame.Rect(
            43 * 2 + (x % 11) * 42, 52 * 2, 37, 15 * len(combination) + 37
        )
    elif row == 1:
        rect = pygame.Rect(
            43 * 2 + (x % 11) * 42,
            52 * 2 + +(15 * len(onTable[x - 11]) + 55),
            37,
            15 * len(combination) + 37,
        )
    else:
        rect = pygame.Rect(
            43 * 2 + (x % 11) * 42,
            52 * 2
            + (15 * len(onTable[x - 11]) + 55)
            + (15 * len(onTable[x - 22]) + 55),
            37,
            15 * len(combination) + 37,
        )
    if rect.collidepoint(getScaledMousePosCards()):
        bloomSurface = pygame.Surface(
            (rect.width + 10, rect.height + 10), pygame.SRCALPHA
        )
        pygame.draw.rect(
            bloomSurface, (0, 150, 255, 100), bloomSurface.get_rect(), border_radius=8
        )
        CardsScreen.blit(bloomSurface, (rect.x - 5, rect.y - 5))


def showCardOnTable(combinationNumber: int, cardPosition: int):
    global onTable, selectedCard, isOnDelPhase
    x = combinationNumber
    y = cardPosition
    row = x // 11
    combination = onTable[combinationNumber]
    if cardPosition < len(combination):
        card = combination[cardPosition]
        if selectedCard.card == None:
            isFirst = False
            if len(onTable[x]) == y + 1:
                if row == 0:
                    rect = pygame.Rect(43 * 2 + (x % 11) * 42, 52 * 2 + y * 15, 37, 52)
                elif row == 1:
                    rect = pygame.Rect(
                        43 * 2 + (x % 11) * 42,
                        52 * 2 + y * 15 + (15 * len(onTable[x - 11]) + 55),
                        37,
                        52,
                    )
                else:
                    rect = pygame.Rect(
                        43 * 2 + (x % 11) * 42,
                        52 * 2
                        + y * 15
                        + (15 * len(onTable[x - 11]) + 55)
                        + (15 * len(onTable[x - 22]) + 55),
                        37,
                        52,
                    )
                isFirst = True
            else:
                if row == 0:
                    rect = pygame.Rect(43 * 2 + (x % 11) * 42, 52 * 2 + y * 15, 37, 15)
                elif row == 1:
                    rect = pygame.Rect(
                        43 * 2 + (x % 11) * 42,
                        52 * 2 + y * 15 + (15 * len(onTable[x - 11]) + 55),
                        37,
                        15,
                    )
                else:
                    rect = pygame.Rect(
                        43 * 2 + (x % 11) * 42,
                        52 * 2
                        + y * 15
                        + (15 * len(onTable[x - 11]) + 55)
                        + (15 * len(onTable[x - 22]) + 55),
                        37,
                        15,
                    )
            if (
                rect.collidepoint(getScaledMousePosCards())
                and not isOnDelPhase
                and not isOnDrawPhase
            ):
                bloomSurface = pygame.Surface(
                    (rect.width + 10, rect.height + (10 if isFirst else 18)),
                    pygame.SRCALPHA,
                )
                pygame.draw.rect(
                    bloomSurface,
                    (0, 150, 255, 100),
                    bloomSurface.get_rect(),
                    border_radius=8,
                )
                CardsScreen.blit(bloomSurface, (rect.x - 5, rect.y - 5))
        if row == 0:
            card.show(CardsScreen, (43 * 2 + (x % 11) * 42, 52 * 2 + y * 15, 37, 52))
        elif row == 1:
            card.show(
                CardsScreen,
                (
                    43 * 2 + (x % 11) * 42,
                    52 * 2 + y * 15 + (15 * len(onTable[x - 11]) + 55),
                    37,
                    52,
                ),
            )
        else:
            card.show(
                CardsScreen,
                (
                    43 * 2 + (x % 11) * 42,
                    52 * 2
                    + y * 15
                    + (15 * len(onTable[x - 11]) + 55)
                    + (15 * len(onTable[x - 22]) + 55),
                    37,
                    52,
                ),
            )


def dropCardOnTable(card: Cards.Card, combinationNumber: int):
    global selectedCard, onTable
    combination = onTable[combinationNumber]
    x = combinationNumber
    row = x // 11
    if row == 0:
        rect = pygame.Rect(
            43 * 2 + (x % 11) * 42, 52 * 2, 37, 15 * len(combination) + 37
        )
    elif row == 1:
        rect = pygame.Rect(
            43 * 2 + (x % 11) * 42,
            52 * 2 + +(15 * len(onTable[x - 11]) + 55),
            37,
            15 * len(combination) + 37,
        )
    else:
        rect = pygame.Rect(
            43 * 2 + (x % 11) * 42,
            52 * 2
            + (15 * len(onTable[x - 11]) + 55)
            + (15 * len(onTable[x - 22]) + 55),
            37,
            15 * len(combination) + 37,
        )
    if rect.collidepoint(getScaledMousePosCards()):
        if selectedCard.card != None:
            rect = pygame.Rect(
                43 * 2 + (combinationNumber % 11) * 42,
                52 * 2
                + combinationNumber
                // 11
                * (
                    15
                    * len(
                        onTable[combinationNumber - 11]
                        if combinationNumber > 10
                        else []
                    )
                    + 55
                ),
                36,
                (15 * len(combination) + 37) / 2,
            )
            if rect.collidepoint(getScaledMousePosCards()):
                combination.insert(0, card)
                onTable[combinationNumber] = combination
            else:
                combination.append(card)
                onTable[combinationNumber] = combination
            onTable[combinationNumber].sort(key=lambda card: (card.value, card.color))
            selectedCard.card = None


def cardToMouse(card: Cards.Card):
    card.show(
        CardsScreen,
        (
            getScaledMousePosCards()[0] - mouseGrabOffset[0],
            getScaledMousePosCards()[1] - mouseGrabOffset[1],
        ),
    )


def isCorectCombination(combination: list[Cards.Card]) -> bool:
    isCorect = False
    # LES CARRES
    if len(combination) == 4 or len(combination) == 3:
        same_value = all(card.value == combination[0].value for card in combination)
        different_colors = len(set(card.color for card in combination)) == len(
            combination
        )
        isCorect = same_value and different_colors
    # LES SUITES
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
                allCombinations.insert(
                    i + 1, combination[len(combination) - 3 : len(combination)]
                )
                combination = combination[0 : len(combination) - 3]
                allCombinations[i] = combination
            if not isCorectCombination(combination):
                return (False, [card.value for card in combination])
        else:
            return (False, [card.value for card in combination])
    return (True, allCombinations)


def selectCardFromHand():
    global \
        selectedCard, \
        mouseGrabOffset, \
        inHand, \
        isOnDelPhase, \
        drawPile, \
        deck, \
        discardPile, \
        isOnDrawPhase
    for i in range(len(inHand)):
        if pygame.Rect(
            16 * 2 + i * 44 + (13 - len(inHand)) * 22, 215 * 2, 37, 52
        ).collidepoint(getScaledMousePosCards()):
            if not isOnDelPhase and not isOnDrawPhase:
                selectedCard.card = inHand[i]
                selectedCard.come = 0
                selectedCard.y = i
                mouseGrabOffset = (
                    getScaledMousePosCards()[0]
                    - (16 * 2 + i * 44 + (13 - len(inHand)) * 22),
                    getScaledMousePosCards()[1] - 210 * 2,
                )
                inHand.remove(selectedCard.card)
            else:
                discardPile.append(inHand.pop(i))
                isOnDelPhase = False
                isOnDrawPhase = True


def selectCardFromTable():
    global selectedCard, mouseGrabOffset, onTable, savedDeck, deck, isOnDelPhase
    if isOnDelPhase or isOnDrawPhase:
        return
    for x in range(len(onTable)):
        for y in range(len(onTable[x])):
            row = x // 11
            if row == 0:
                rect = pygame.Rect(
                    43 * 2 + (x % 11) * 42,
                    52 * 2 + y * 15,
                    37,
                    52 if len(onTable[x]) == y + 1 else 15,
                )
            elif row == 1:
                rect = pygame.Rect(
                    43 * 2 + (x % 11) * 42,
                    52 * 2 + y * 15 + (15 * len(onTable[x - 11]) + 55),
                    37,
                    52 if len(onTable[x]) == y + 1 else 15,
                )
            else:
                rect = pygame.Rect(
                    43 * 2 + (x % 11) * 42,
                    52 * 2
                    + y * 15
                    + (15 * len(onTable[x - 11]) + 55)
                    + (15 * len(onTable[x - 22]) + 55),
                    37,
                    52 if len(onTable[x]) == y + 1 else 15,
                )
            if rect.collidepoint(getScaledMousePosCards()):
                savedDeck = deck.saveDeck()
                selectedCard.card = onTable[x][y]
                selectedCard.come = 1
                selectedCard.x = x
                selectedCard.y = y
                mouseGrabOffset = (
                    getScaledMousePosCards()[0] - rect.x,
                    getScaledMousePosCards()[1] - rect.y,
                )
                left = onTable[x][:y]
                right = onTable[x][y + 1 :]
                onTable[x] = left
                onTable.insert(x + 1, right)
                suppEmptyCombinations()
                return


def suppEmptyCombinations():
    global onTable
    onTable = [combination for combination in onTable if len(combination) > 0]

    #   --- INITIALISATION PYGAME ---  #


pygame.init()
screen = pygame.display.set_mode(
    (GetSystemMetrics(0), GetSystemMetrics(1)), pygame.FULLSCREEN
)


#   ----- ADAPTER RESOLUTION ----  #
resoCible = [315, 250]
resolution = [GetSystemMetrics(0), GetSystemMetrics(1)]
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
UIScreen = pygame.Surface((resoCible[0], resoCible[1]))
CardsScreen = pygame.Surface((resolution[0], resolution[1]), pygame.SRCALPHA)

#   --------- LES IMAGES --------  #
backgroundMain = pygame.image.load("Assets\\MainMenu\\BackGround.png")
backgroundMain = backgroundMain.convert()

jeton2TileMap = pygame.image.load("Assets\\MainMenu\\Jeton\\jeton2TileMap.png")
jeton2Tiles = [jeton2TileMap.subsurface(x, 0, 64, 72) for x in range(0, 256, 64)]
jeton2rect = pygame.Rect(196, 49, 64, 72)
jeton2 = jeton2Tiles[0]

jeton1TileMap = pygame.image.load("Assets\\MainMenu\\Jeton\\jeton1TileMap.png")
jeton1Tiles = [jeton1TileMap.subsurface(x, 0, 69, 61) for x in range(0, 552, 69)]
jeton1rect = pygame.Rect(41, 58, 69, 61)
jeton1 = jeton1Tiles[0]

diceTileMap = pygame.image.load("Assets\\MainMenu\\DiceTileMap.png")
diceTiles = [diceTileMap.subsurface(0, y, 64, 16) for y in range(0, 118, 16)]

playButtonTileMap = pygame.image.load("Assets\\MainMenu\\Button\\PlayTileMap.png")
playButtonTiles = [
    playButtonTileMap.subsurface(x, 0, 86, 48) for x in range(0, 774, 86)
]
teamButtonTileMap = pygame.image.load("Assets\\MainMenu\\Button\\TeamTileMap.png")
teamButtonTiles = [
    teamButtonTileMap.subsurface(x, 0, 86, 48) for x in range(0, 774, 86)
]

cardsBox = pygame.image.load("Assets\\MainMenu\\CardsBox.png")
cardsDeck = pygame.image.load("Assets\\MainMenu\\CardsDeck.png")
drawPileAssets = pygame.image.load(
    "Assets\\Cards\\King's Cards\\Back And Joker\\DrawPile.png"
)
backCard = pygame.image.load("Assets\\Cards\\King's Cards\\Back And Joker\\Back_1.png")


#   ------ LES ANNIMATIONS ------  #
annimationPlayButton_actuelFrame = 0
annimationPlayButton_isMouseOn = False


def annimationPlayButton():
    global annimationPlayButton_actuelFrame, annimationPlayButton_isMouseOn
    actuelFrame = annimationPlayButton_actuelFrame
    isMouseOn = playButton.rect.collidepoint(getScaledMousePosUI())
    if isMouseOn and actuelFrame < len(playButtonTiles) - 1:
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
    if isMouseOn and actuelFrame < len(teamButtonTiles) - 1:
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
    if isMouseOn and actuelFrame < len(jeton1Tiles) - 1:
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
    if isMouseOn and actuelFrame < len(jeton2Tiles) - 1:
        actuelFrame += 1
        jeton2 = jeton2Tiles[actuelFrame]
    elif not isMouseOn and actuelFrame > 0:
        actuelFrame -= 1
        jeton2 = jeton2Tiles[actuelFrame]
    annimationJeton2_isMouseOn = isMouseOn
    annimationJeton2_actuelFrame = actuelFrame


annimationDice_actuelFrame = 0
annimationDice_isMouseOn = False
annimationDice_lastFram = 0


def annimationDice():
    global \
        annimationDice_actuelFrame, \
        annimationDice_isMouseOn, \
        annimationDice_lastFram, \
        nextTurnButton, \
        selectedCard
    if selectedCard.card == None and time.time() - annimationDice_lastFram > 0.1:
        actuelFrame = annimationDice_actuelFrame
        isMouseOn = nextTurnButton.rect.collidepoint(getScaledMousePosUI())
        if isMouseOn and actuelFrame < len(diceTiles) - 1:
            actuelFrame += 1
            nextTurnButton.setImage(diceTiles[actuelFrame])
        elif not isMouseOn:
            actuelFrame = 0
            nextTurnButton.setImage(diceTiles[actuelFrame])
        annimationDice_isMouseOn = isMouseOn
        annimationDice_actuelFrame = actuelFrame
        annimationDice_lastFram = time.time()

        #   --------- LES BOUTONS --------  #


# LEURS FONCTIONS
def playButtonClic():
    global UIScreen, resoCible, resolution, isOnMainMenu
    isOnMainMenu = False
    UIScreen = pygame.transform.scale(UIScreen, (resoCible[0], resoCible[1]))
    pygame.draw.rect(
        UIScreen, (255, 255, 255), pygame.Rect(0, 0, resoCible[0], resoCible[1])
    )
    UIScreen = pygame.transform.scale(UIScreen, (resolution[0], resolution[1]))
    teamButton.isActive = False
    playButton.isActive = False


def teamButtonClic():
    print("Team Pressed")


def nextTurnButtonClic():
    global drawPile, onTable, isOnDelPhase
    isOK, newTable = checkCombinations(deck.onTable)
    if isOK:
        onTable = newTable
        isOnDelPhase = True


def drawPileButtonClic():
    global inHand, drawPile, isOnDrawPhase
    if isOnDrawPhase:
        inHand.append(drawPile.pop())
        isOnDrawPhase = False


def discardPileButton():
    global inHand, discardPile, isOnDrawPhase
    if isOnDrawPhase:
        inHand.append(discardPile.pop())
        isOnDrawPhase = False


# LES BOUTONS
playButton = UI.Button(
    pygame.Rect(125, 65, 64, 48),
    (11, 0),
    "PlayButton",
    playButtonTiles[0],
    playButtonClic,
)
teamButton = UI.Button(
    pygame.Rect(125, 144, 64, 48),
    (11, 0),
    "TeamButton",
    teamButtonTiles[0],
    teamButtonClic,
)
nextTurnButton = UI.Button(
    pygame.Rect(125, 198, 64, 16),
    (0, 0),
    "NextTurnButton",
    diceTiles[0],
    nextTurnButtonClic,
)
drawPileButton = UI.Button(
    pygame.Rect(275, 99, 37, 60),
    (0, 0),
    "DrawPileButton",
    drawPileAssets,
    drawPileButtonClic,
)
discardPileButton = UI.Button(
    pygame.Rect(3, 99, 37, 60),
    (0, 0),
    "DiscardPileButton",
    drawPileAssets,
    discardPileButton,
)
allButton = [playButton, teamButton, nextTurnButton, drawPileButton, discardPileButton]

#   ------- BOUCLE DE JEU -------  #
deck = Cards.Deck()
deck.shuffleDeck()
for i in range(13):
    cardTest = deck.pickCard()
    deck.inHand.append(cardTest)
for i in range(1):
    cardTest = deck.pickCard()
    deck.inOpponentHand.append(cardTest)
"""tmp=[]
for i in range(24):
    for j in range(3):
        cardTest = deck.pickCard()
        tmp.append(cardTest)
    deck.onTable.append(tmp)
    tmp = []"""
deck.inDiscardPile.append(deck.pickCard())

selectedCard = Cards.cardSelected(None, 0, 0)
selectedCard.y = 0
run = True
isOnMainMenu = True
isOnDelPhase = False
isOnDrawPhase = False
mouseGrabOffset = [0, 0]
savedDeck = None
while run:
    drawPile = deck.drawPile
    onTable = deck.onTable
    inHand = deck.inHand
    inOpponentHand = deck.inOpponentHand
    discardPile = deck.inDiscardPile

    # LES EVENTS
    for event in pygame.event.get():
        if (
            event.type == pygame.QUIT
            or event.type == pygame.KEYDOWN
            and event.key == pygame.K_ESCAPE
        ):
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in allButton:
                button.isClic(resoCible, resolution, offsets)
            selectCardFromHand()
            selectCardFromTable()

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            for i in range(len(onTable)):
                dropCardOnTable(selectedCard.card, i)
                if selectedCard.card == None:
                    break
            if selectedCard.card != None:
                if pygame.Rect(37 * 2, 60 * 2, 241 * 2, 138 * 2).collidepoint(
                    getScaledMousePosCards()
                ):
                    onTable.append([selectedCard.card])
                elif selectedCard.come == 0:
                    inHand.insert(selectedCard.y, selectedCard.card)
                else:
                    onTable = savedDeck.onTable
            selectedCard.card = None

        if (
            event.type == pygame.MOUSEBUTTONUP
            and event.button == 3
            and selectedCard.card != None
        ):
            if selectedCard.come == 0:
                inHand.insert(selectedCard.y, selectedCard.card)
            else:
                onTable = savedDeck.onTable
            selectedCard.card = None

    # LES GRAPHISMES
    UIScreen = pygame.transform.scale(UIScreen, (resoCible[0], resoCible[1]))
    CardsScreen = pygame.transform.scale(
        CardsScreen, (resoCible[0] * 2, resoCible[1] * 2)
    )
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
        drawPileButton.show(UIScreen)
        discardPileButton.show(UIScreen)
        discardPile[-1].show(UIScreen, (3, 99))

        if not isOnDelPhase and not isOnDrawPhase:
            nextTurnButton.show(UIScreen)
            annimationDice()

        # Les cartes sur la table
        for x in range(len(onTable)):
            if selectedCard.card != None:
                bloomCombination(x)
            for y in range(len(onTable[x])):
                showCardOnTable(x, y)

        # les cartes en main
        for i in range(len(inHand)):
            if (
                pygame.Rect(
                    16 * 2 + i * 44 + (13 - len(inHand)) * 22, 215 * 2, 37, 52
                ).collidepoint(getScaledMousePosCards())
                and selectedCard.card == None
            ):
                inHand[i].show(
                    CardsScreen,
                    (16 * 2 + i * 44 + (13 - len(inHand)) * 22, 210 * 2),
                    (0, 150, 255, 100) if not isOnDelPhase else (255, 0, 0, 100),
                )
            else:
                inHand[i].show(
                    CardsScreen, (16 * 2 + i * 44 + (13 - len(inHand)) * 22, 215 * 2)
                )
        for i in range(len(inOpponentHand)):
            CardsScreen.blit(
                backCard,
                (90 * 2 + i * 32 + (13 - len(inOpponentHand)) * 22, 4 * 2 + i * 3),
            )
        cardToMouse(selectedCard.card) if selectedCard.card != None else None

    UIScreen = pygame.transform.scale(UIScreen, (resolution[0], resolution[1]))
    CardsScreen = pygame.transform.scale(CardsScreen, (resolution[0], resolution[1]))
    UIScreen.blit(CardsScreen, (0, 0))

    screen.blit(UIScreen, (offsets[0], offsets[1]))

    suppEmptyCombinations()
    deck.onTable = onTable
    deck.inHand = inHand
    deck.inOpponentHand = inOpponentHand
    deck.drawPile = drawPile
    deck.inDiscardPile = discardPile

    pygame.display.flip()
    time.sleep(0.01)

pygame.quit()

