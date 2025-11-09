import pygame
import UI
import Cards
import os

# from win32api import GetSystemMetrics
import time
# numpy est neccessaire pour la fonction bloomCombination mais pas besion d'import


#   ------- FONCTION CLEE -------  #
def resetTurn():
    global deck, allSavedDeck, onTable, drawPile, discardPile, inOpponentHand, inHand, isOnDrawPhase
    if len(allSavedDeck) != 0 and not (isOnDelPhase or isOnDrawPhase):
        check = discardPile[-1]
        deck = allSavedDeck[0]
        allSavedDeck = []
        drawPile = deck.drawPile
        onTable = deck.onTable
        inHand = deck.inHand
        inOpponentHand = deck.inOpponentHand
        discardPile = deck.inDiscardPile
        if check != discardPile[-1]:
            isOnDrawPhase = True
def undo():
    global deck, allSavedDeck, onTable, drawPile, discardPile, inOpponentHand, inHand, isOnDrawPhase
    if len(allSavedDeck) != 0 and not (isOnDelPhase or isOnDrawPhase):
        check = discardPile[-1]
        deck = allSavedDeck.pop()
        drawPile = deck.drawPile
        onTable = deck.onTable
        inHand = deck.inHand
        inOpponentHand = deck.inOpponentHand
        discardPile = deck.inDiscardPile
        if check != discardPile[-1]:
            isOnDrawPhase = True

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
    global selectedCard, onTable, allSavedDeck, savedDeck, doDropCard
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
            combination.append(card)
            combination.sort(key=lambda card: (card.value, card.color))
            if len(combination) != 6:
                onTable[combinationNumber] = combination
            else:
                onTable[combinationNumber] = combination[:3]
                onTable.insert(combinationNumber+1, combination[3:])
            selectedCard.card = None
            doDropCard = True


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
    if cardDrawOnDiscardPile == None or not (cardDrawOnDiscardPile in inHand):
        return (True, allCombinations)
    return (False, allCombinations)


def selectCardFromHand():
    global \
        selectedCard, \
        mouseGrabOffset, \
        inHand, \
        isOnDelPhase, \
        drawPile, \
        deck, \
        discardPile, \
        isOnDrawPhase, \
        savedDeck
    for i in range(len(inHand)):
        if pygame.Rect(
            16 * 2 + i * 44 + (13 - len(inHand)) * 22, 215 * 2, 37, 52
        ).collidepoint(getScaledMousePosCards()):
            if not isOnDelPhase and not isOnDrawPhase:
                savedDeck = deck.saveDeck()
                selectedCard.card = inHand[i]
                selectedCard.come = 0
                selectedCard.y = i
                mouseGrabOffset = (
                    getScaledMousePosCards()[0]
                    - (16 * 2 + i * 44 + (13 - len(inHand)) * 22),
                    getScaledMousePosCards()[1] - 210 * 2,
                )
                inHand.remove(selectedCard.card)
            elif isOnDelPhase:
                discardPile.append(inHand.pop(i))
                isOnDelPhase = False
                isOnDrawPhase = True


def suppEmptyCombinations():
    global onTable
    onTable = [combination for combination in onTable if len(combination) > 0]

    #   --- INITIALISATION PYGAME ---  #


pygame.init()
screen_info = pygame.display.Info()
screen = pygame.display.set_mode(
    (screen_info.current_w, screen_info.current_h), pygame.FULLSCREEN
)


#   ----- ADAPTER RESOLUTION ----  #
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
UIScreen = pygame.Surface((resoCible[0], resoCible[1]))
CardsScreen = pygame.Surface((resolution[0], resolution[1]), pygame.SRCALPHA)
RuleScreen = pygame.Surface((resoCible[0]*3, resoCible[1]*3), pygame.SRCALPHA)

#   --------- LES IMAGES --------  #
backgroundMain = pygame.image.load("Assets/MainMenu/BackGround.png")
backgroundMain = backgroundMain.convert()

jeton2TileMap = pygame.image.load("Assets/MainMenu/Jeton/Jeton2TileMap.png")
jeton2Tiles = [jeton2TileMap.subsurface(x, 0, 64, 72) for x in range(0, 256, 64)]
jeton2rect = pygame.Rect(196, 49, 64, 72)
jeton2 = jeton2Tiles[0]

jeton1TileMap = pygame.image.load("Assets/MainMenu/Jeton/Jeton1TileMap.png")
jeton1Tiles = [jeton1TileMap.subsurface(x, 0, 69, 61) for x in range(0, 552, 69)]
jeton1rect = pygame.Rect(41, 58, 69, 61)
jeton1 = jeton1Tiles[0]

diceTileMap = pygame.image.load("Assets/MainMenu/DiceTileMap.png")
diceTiles = [diceTileMap.subsurface(0, y, 64, 16) for y in range(0, 118, 16)]

rules = pygame.image.load("Assets/MainMenu/RuleMenu.png")

playButtonTileMap = pygame.image.load("Assets/MainMenu/Button/PlayTileMap.png")
playButtonTiles = [
    playButtonTileMap.subsurface(x, 0, 86, 48) for x in range(0, 774, 86)
]
teamButtonTileMap = pygame.image.load("Assets/MainMenu/Button/TeamTileMap.png")
teamButtonTiles = [
    teamButtonTileMap.subsurface(x, 0, 86, 48) for x in range(0, 774, 86)
]
ruleButtonTileMap = pygame.image.load("Assets/MainMenu/Button/RuleTileMap.png")
ruleButtonTiles = [
    ruleButtonTileMap.subsurface(x, 0, 86, 48) for x in range(0, 774, 86)
]

cardsBox = pygame.image.load("Assets/MainMenu/CardsBox.png")
cardsDeck = pygame.image.load("Assets/MainMenu/CardsDeck.png")
drawPileAssets = pygame.image.load(
    "Assets/Cards/King's Cards/Back And Joker/DrawPile.png"
)
backCard = pygame.image.load("Assets/Cards/King's Cards/Back And Joker/Back_1.png")


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


annimationRuleButton_actuelFrame = 0
annimationRuleButton_isMouseOn = False


def annimationRuleButton():
    global annimationRuleButton_actuelFrame, annimationRuleButton_isMouseOn
    actuelFrame = annimationRuleButton_actuelFrame
    isMouseOn = ruleButton.rect.collidepoint(getScaledMousePosUI())
    if isMouseOn and actuelFrame < len(ruleButtonTiles) - 1:
        actuelFrame += 1
        ruleButton.setImage(ruleButtonTiles[actuelFrame])
    elif not isMouseOn and actuelFrame > 0:
        actuelFrame -= 1
        ruleButton.setImage(ruleButtonTiles[actuelFrame])
    annimationRuleButton_isMouseOn = isMouseOn
    annimationRuleButton_actuelFrame = actuelFrame


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


def ruleButtonClic():
    global isOnRuleScreen, allButton
    isOnRuleScreen = True
    for button in allButton:
        button.isActive = False

def nextTurnButtonClic():
    global drawPile, onTable, isOnDelPhase, doDropCard, allSavedDeck, isOnDrawPhase
    isOK, newTable = checkCombinations(deck.onTable)
    if isOK and not (isOnDelPhase or isOnDrawPhase):
        onTable = newTable
        allSavedDeck = []
        if not doDropCard:
            isOnDelPhase = True
        else:
            isOnDrawPhase = True
        doDropCard = False


def drawPileButtonClic():
    global inHand, drawPile, isOnDrawPhase, cardDrawOnDiscardPile, allSavedDeck, deck
    if isOnDrawPhase:
        cardDrawOnDiscardPile = None
        inHand.append(drawPile.pop())
        isOnDrawPhase = False
        inHand.sort(key=lambda c: (c.color, c.value))
        allSavedDeck = [deck.saveDeck()]


def discardPileButton():
    global inHand, discardPile, isOnDrawPhase, cardDrawOnDiscardPile, deck, allSavedDeck
    if isOnDrawPhase:
        allSavedDeck = [deck.saveDeck()]
        cardDrawOnDiscardPile = discardPile.pop()
        inHand.append(cardDrawOnDiscardPile)
        isOnDrawPhase = False
        inHand.sort(key=lambda c: (c.color, c.value))


# LES BOUTONS
playButton = UI.Button(
    pygame.Rect(125, 53, 64, 48),
    (11, 0),
    "PlayButton",
    playButtonTiles[0],
    playButtonClic,
)
teamButton = UI.Button(
    pygame.Rect(125, 159, 64, 48),
    (11, 0),
    "TeamButton",
    teamButtonTiles[0],
    teamButtonClic,
)
ruleButton = UI.Button(
    pygame.Rect(125, 105, 64, 48),
    (11, 0),
    "RuleButton",
    ruleButtonTiles[0],
    ruleButtonClic,
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
allButton = [playButton, teamButton, ruleButton, nextTurnButton, drawPileButton, discardPileButton]

#   ------- BOUCLE DE JEU -------  #
deck = Cards.Deck()
deck.shuffleDeck()
for i in range(13):
    cardTest = deck.pickCard()
    deck.inHand.append(cardTest)
deck.inHand.sort(key=lambda c: (c.color, c.value))
for i in range(1):
    cardTest = deck.pickCard()
    deck.inOpponentHand.append(cardTest)
deck.inDiscardPile.append(deck.pickCard())

selectedCard = Cards.cardSelected(None, 0, 0)
selectedCard.y = 0
run = True
isOnRuleScreen = False
isOnMainMenu = True
isOnDelPhase = False
isOnDrawPhase = False
doDropCard = False
cardDrawOnDiscardPile: Cards.Card = None
mouseGrabOffset = [0, 0]
savedDeck = None
allSavedDeck: list[Cards.Deck] = []
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

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            if isOnRuleScreen:
                isOnRuleScreen = False
                for button in allButton:
                    button.isActive = True

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            for i in range(len(onTable)):
                dropCardOnTable(selectedCard.card, i)
                if selectedCard.card == None:
                    allSavedDeck.append(savedDeck)
                    break
            if selectedCard.card != None:
                if pygame.Rect(37 * 2, 60 * 2, 241 * 2, 138 * 2).collidepoint(
                    getScaledMousePosCards()
                ):
                    onTable.append([selectedCard.card])
                    allSavedDeck.append(savedDeck)
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
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_z and (event.mod & pygame.KMOD_CTRL):
            undo()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            resetTurn()

    # LES GRAPHISMES
    UIScreen = pygame.transform.scale(UIScreen, (resoCible[0], resoCible[1]))
    CardsScreen = pygame.transform.scale(
        CardsScreen, (resoCible[0] * 2, resoCible[1] * 2)
    )
    UIScreen.fill((0, 0, 0))
    CardsScreen.fill((0, 0, 0, 0))
    RuleScreen.fill((0, 0, 0, 0))

    if isOnMainMenu:
        UIScreen.blit(backgroundMain, (0, 0))
        UIScreen.blit(cardsBox, (35, 126))
        UIScreen.blit(cardsDeck, (231, 127))
        UIScreen.blit(jeton2, (jeton2rect.x, jeton2rect.y))
        UIScreen.blit(jeton1, (jeton1rect.x, jeton1rect.y))
        playButton.show(UIScreen)
        teamButton.show(UIScreen)
        ruleButton.show(UIScreen)

        if isOnRuleScreen:
            RuleScreen = pygame.transform.scale(RuleScreen, (resoCible[0]*3, resoCible[1]*3))
            RuleScreen.blit(rules, (0, 0))
            RuleScreen = pygame.transform.scale(RuleScreen, (resolution[0], resolution[1]))
        else:
            annimationRuleButton()
            annimationTeamButton()
            annimationPlayButton()
            annimationJeton1()
            annimationJeton2()

    else:
        UIScreen.blit(backgroundMain, (0, 0))
        drawPileButton.show(UIScreen)
        if len(discardPile) != 0: discardPileButton.show(UIScreen)
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
    UIScreen.blit(RuleScreen, (0, 0))


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
