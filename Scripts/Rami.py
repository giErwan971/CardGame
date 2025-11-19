import pygame
import Cards
from utils import *



def resetTurn(deck, allSavedDeck, onTable, drawPile, discardPile, inOpponentHand, inHand, isOnDrawPhase, isOnDelPhase):
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
def undo(deck, allSavedDeck, onTable, drawPile, discardPile, inOpponentHand, inHand, isOnDrawPhase, isOnDelPhase):
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


def bloomCombination(combinationNumber: int, onTable, CardsScreen):
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


def showCardOnTable(combinationNumber: int, cardPosition: int, onTable, selectedCard, isOnDelPhase, isOnDrawPhase, CardsScreen):
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


def dropCardOnTable(card: Cards.Card, combinationNumber: int, selectedCard, onTable, allSavedDeck, savedDeck, doDropCard):
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


def cardToMouse(card: Cards.Card, CardsScreen, mouseGrabOffset):
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


def checkCombinations(allCombinations: list[list[Cards.Card]], cardDrawOnDiscardPile, inHand) -> tuple:
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


def selectCardFromHand(selectedCard, mouseGrabOffset, inHand, isOnDelPhase,drawPile, deck, discardPile,isOnDrawPhase,savedDeck):
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

def suppEmptyCombinations(onTable):
    onTable = [combination for combination in onTable if len(combination) > 0]