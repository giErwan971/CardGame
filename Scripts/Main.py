import pygame
import UI
import Cards
import Rami
import utils
import Bot
# from win32api import GetSystemMetrics
import time
# numpy est neccessaire pour la fonction bloomCombination mais pas besion d'import


#   ------- FONCTION CLEE -------  #


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
RuleScreen = pygame.Surface((resoCible[0] * 3, resoCible[1] * 3), pygame.SRCALPHA)
utils.init(resoCible, resolution, offsets)

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
teamImage = pygame.image.load("Assets/MainMenu/TeamMenu.png")

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

victory = pygame.image.load("Assets/MainMenu/Victory.png")
defeat = pygame.image.load("Assets/MainMenu/Defeat.png")


#   ------ LES ANNIMATIONS ------  #
annimationPlayButton_actuelFrame = 0
annimationPlayButton_isMouseOn = False


def annimationPlayButton():
    global annimationPlayButton_actuelFrame, annimationPlayButton_isMouseOn
    actuelFrame = annimationPlayButton_actuelFrame
    isMouseOn = playButton.rect.collidepoint(utils.getScaledMousePosUI())
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
    isMouseOn = teamButton.rect.collidepoint(utils.getScaledMousePosUI())
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
    isMouseOn = ruleButton.rect.collidepoint(utils.getScaledMousePosUI())
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
    isMouseOn = jeton1rect.collidepoint(utils.getScaledMousePosUI())
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
    isMouseOn = jeton2rect.collidepoint(utils.getScaledMousePosUI())
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
        isMouseOn = nextTurnButton.rect.collidepoint(utils.getScaledMousePosUI())
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
    global isOnTeamScreen, allButton
    isOnTeamScreen = True
    for button in allButton:
        button.isActive = False


def ruleButtonClic():
    global isOnRuleScreen, allButton
    isOnRuleScreen = True
    for button in allButton:
        button.isActive = False


def nextTurnButtonClic():
    global isOnDelPhase, doDropCard, allSavedDeck, isOnDrawPhase, deck, whoWin, UIScreen, run
    isOK, newTable = Rami.checkCombinations(deck.onTable, cardDrawOnDiscardPile, deck.inHand)
    if isOK and not (isOnDelPhase or isOnDrawPhase):
        deck.onTable = newTable
        allSavedDeck = []
        if not doDropCard:
            isOnDelPhase = True
        else:
            deck = Bot.playTurn(deck)
            isOnDrawPhase = True
        doDropCard = False
        if len(deck.inHand) == 0:
            whoWin = "Player"
            UIScreen.blit(victory, (91, 95))
            run = False


def drawPileButtonClic():
    global isOnDrawPhase, cardDrawOnDiscardPile, allSavedDeck, deck, pickedCard
    if isOnDrawPhase:
        cardDrawOnDiscardPile = None
        pickedCard = deck.drawPile.pop()
        deck.inHand.append(pickedCard)
        isOnDrawPhase = False
        deck.inHand.sort(key=lambda c: (c.color, c.value))
        allSavedDeck = [deck.saveDeck()]



def inDiscardPileButton():
    global isOnDrawPhase, cardDrawOnDiscardPile, deck, allSavedDeck, pickedCard
    if isOnDrawPhase:
        allSavedDeck = [deck.saveDeck()]
        cardDrawOnDiscardPile = deck.inDiscardPile.pop()
        pickedCard = cardDrawOnDiscardPile
        deck.inHand.append(cardDrawOnDiscardPile)
        isOnDrawPhase = False
        deck.inHand.sort(key=lambda c: (c.color, c.value))


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
inDiscardPileButton = UI.Button(
    pygame.Rect(3, 99, 37, 60),
    (0, 0),
    "DiscardPileButton",
    drawPileAssets,
    inDiscardPileButton,
)
allButton = [
    playButton,
    teamButton,
    ruleButton,
    nextTurnButton,
    drawPileButton,
    inDiscardPileButton,
]

#   ------- BOUCLE DE JEU -------  #
deck = Cards.Deck()
deck.shuffleDeck()
for i in range(13):
    cardTest = deck.pickCard()
    deck.inHand.append(cardTest)
deck.inHand.sort(key=lambda c: (c.color, c.value))
for i in range(13):
    cardTest = deck.pickCard()
    deck.inOpponentHand.append(cardTest)
deck.inDiscardPile.append(deck.pickCard())

selectedCard = Cards.cardSelected(None, 0, 0)
selectedCard.y = 0
run = True
isOnRuleScreen = False
isOnTeamScreen = False
isOnMainMenu = True
isOnDelPhase = False
isOnDrawPhase = False
doDropCard = False
cardDrawOnDiscardPile: Cards.Card = None
mouseGrabOffset = [0, 0]
savedDeck = None
allSavedDeck: list[Cards.Deck] = []
pickedCard = None
whoWin = None
while run:
    if len(deck.drawPile) == 0:
        tmp = deck.inDiscardPile.pop()
        deck.drawPile = deck.inDiscardPile.copy()
        deck.inDiscardPile = []
        deck.shuffleDeck()
        deck.inDiscardPile.append(tmp)
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
            savedDeck, mouseGrabOffset, isOnDrawPhase, isOnDelPhase, selectedCard, deck, isLose = Rami.selectCardFromHand(
                selectedCard,
                mouseGrabOffset,
                deck.inHand,
                isOnDelPhase,
                deck,
                deck.inDiscardPile,
                isOnDrawPhase,
                savedDeck,
            )
            if isLose:
                whoWin = "Bot"

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            if isOnRuleScreen:
                isOnRuleScreen = False
                for button in allButton:
                    button.isActive = True
            if isOnTeamScreen:
                isOnTeamScreen = False
                for button in allButton:
                    button.isActive = True

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            for i in range(len(deck.onTable)):
                doDropCard = Rami.dropCardOnTable(
                    selectedCard.card,
                    i,
                    selectedCard,
                    deck.onTable,
                    doDropCard,
                )
                if selectedCard.card == None:
                    allSavedDeck.append(savedDeck)
                    break
            if selectedCard.card != None:
                if pygame.Rect(37 * 2, 60 * 2, 241 * 2, 138 * 2).collidepoint(
                    utils.getScaledMousePosCards()
                ):
                    deck.onTable.append([selectedCard.card])
                    allSavedDeck.append(savedDeck)
                elif selectedCard.come == 0:
                    deck.inHand.insert(selectedCard.y, selectedCard.card)
                else:
                    deck.onTable = savedDeck.deck.onTable
            selectedCard.card = None

        if (
            event.type == pygame.MOUSEBUTTONUP
            and event.button == 3
            and selectedCard.card != None
        ):
            if selectedCard.come == 0:
                deck.inHand.insert(selectedCard.y, selectedCard.card)
            else:
                deck.onTable = savedDeck.deck.onTable
            selectedCard.card = None

        if (
            event.type == pygame.KEYDOWN
            and event.key == pygame.K_z
            and (event.mod & pygame.KMOD_CTRL)
        ):
            deck, isOnDrawPhase, allSavedDeck = Rami.undo(
                deck,
                allSavedDeck,
                deck.inDiscardPile,
                isOnDrawPhase,
                isOnDelPhase,
            )
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            deck, isOnDrawPhase, allSavedDeck = Rami.resetTurn(
                deck,
                allSavedDeck,
                deck.inDiscardPile,
                isOnDrawPhase,
                isOnDelPhase,
            )

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
            RuleScreen = pygame.transform.scale(
                RuleScreen, (resoCible[0] * 3, resoCible[1] * 3)
            )
            RuleScreen.blit(rules, (0, 0))
            RuleScreen = pygame.transform.scale(
                RuleScreen, (resolution[0], resolution[1])
            )
        if isOnTeamScreen:
            RuleScreen = pygame.transform.scale(
                RuleScreen, (resoCible[0] * 3, resoCible[1] * 3)
            )
            RuleScreen.blit(teamImage, (0, 0))
            RuleScreen = pygame.transform.scale(
                RuleScreen, (resolution[0], resolution[1])
            )
        else:
            annimationRuleButton()
            annimationTeamButton()
            annimationPlayButton()
            annimationJeton1()
            annimationJeton2()

    else:
        UIScreen.blit(backgroundMain, (0, 0))
        if isOnDrawPhase:
            bloomSurface = pygame.Surface(
                ((drawPileButton.rect.width + 10), (drawPileButton.rect.height + 10)),
                pygame.SRCALPHA,
            )
            pygame.draw.rect(
                bloomSurface, (0, 255, 150, 100), bloomSurface.get_rect(), border_radius=8
            )
            UIScreen.blit(bloomSurface, (drawPileButton.rect.x - 5, drawPileButton.rect.y - 5))
        drawPileButton.show(UIScreen)
        if len(deck.inDiscardPile) != 0:
            if isOnDrawPhase:
                bloomSurface = pygame.Surface(
                    ((inDiscardPileButton.rect.width + 10), (inDiscardPileButton.rect.height + 10)),
                    pygame.SRCALPHA,
                )
                pygame.draw.rect(
                    bloomSurface, (0, 255, 150, 100), bloomSurface.get_rect(), border_radius=8
                )
                UIScreen.blit(bloomSurface, (inDiscardPileButton.rect.x - 5, inDiscardPileButton.rect.y - 5))
            inDiscardPileButton.show(UIScreen)
            deck.inDiscardPile[-1].show(UIScreen, (3, 99))

        if not isOnDelPhase and not isOnDrawPhase:
            nextTurnButton.show(UIScreen)
            annimationDice()

        # Les cartes sur la table
        for x in range(len(deck.onTable)):
            if selectedCard.card != None:
                Rami.bloomCombination(x, deck.onTable, CardsScreen)
            for y in range(len(deck.onTable[x])):
                Rami.showCardOnTable(
                    x,
                    y,
                    deck.onTable,
                    selectedCard,
                    isOnDelPhase,
                    isOnDrawPhase,
                    CardsScreen,
                )
        # les cartes en main
        for i in range(len(deck.inHand)):
            if (
                pygame.Rect(
                    16 * 2 + i * 44 + (13 - len(deck.inHand)) * 22, 215 * 2, 37, 52
                ).collidepoint(utils.getScaledMousePosCards())
                and selectedCard.card == None and not isOnDrawPhase
            ):
                deck.inHand[i].show(
                    CardsScreen,
                    (16 * 2 + i * 44 + (13 - len(deck.inHand)) * 22, 210 * 2),
                    (0, 150, 255, 100) if not isOnDelPhase else (255, 0, 0, 100),
                )
            
            elif deck.inHand[i] == pickedCard:
                deck.inHand[i].show(
                    CardsScreen,
                    (16 * 2 + i * 44 + (13 - len(deck.inHand)) * 22, 215 * 2),
                    (0, 255, 150, 100),
                )
            else:
                deck.inHand[i].show(
                    CardsScreen, (16 * 2 + i * 44 + (13 - len(deck.inHand)) * 22, 215 * 2)
                )
            
        for i in range(len(deck.inOpponentHand)):
            CardsScreen.blit(
                backCard,
                (90 * 2 + i * 32 + (13 - len(deck.inOpponentHand)) * 22, 4 * 2 + i * 3),
            )
        Rami.cardToMouse(
            selectedCard.card, CardsScreen, mouseGrabOffset
        ) if selectedCard.card != None else None

    UIScreen = pygame.transform.scale(UIScreen, (resolution[0], resolution[1]))
    CardsScreen = pygame.transform.scale(CardsScreen, (resolution[0], resolution[1]))
    UIScreen.blit(CardsScreen, (0, 0))
    UIScreen.blit(RuleScreen, (0, 0))

    screen.blit(UIScreen, (offsets[0], offsets[1]))

    deck.onTable = Rami.suppEmptyCombinations(deck.onTable)

    pygame.display.flip()
    time.sleep(0.01)

if whoWin != None:
    run = True
    UIScreen = pygame.transform.scale(UIScreen, (resoCible[0], resoCible[1]))
    UIScreen.blit(backgroundMain, (0, 0))
    if whoWin == "Player":
        UIScreen.blit(victory, (91, 95))
    else:
        UIScreen.blit(defeat, (91, 95))
    UIScreen = pygame.transform.scale(UIScreen, (resolution[0], resolution[1]))
    screen.blit(UIScreen, (offsets[0], offsets[1]))
    pygame.display.flip()
while run:
    for event in pygame.event.get():
        if (
            event.type == pygame.QUIT
            or event.type == pygame.KEYDOWN
            and event.key == pygame.K_ESCAPE
        ):
            run = False
pygame.quit()
