from random import *
import pygame
from pygame.rect import Rect


class Card:
    def __init__(self, value, color, etat):
        self.value = value
        self.color = color
        self.etat = (
            etat  # 0 = in draw pile, 1 = in hand, 2 = in opponent hand, 3 = on table
        )
        self.bg = pygame.image.load(
            f"Assets/Cards/King's Cards/Suit Of {color}/{color}_{value}.png"
        )
        pygame.transform.scale2x(self.bg)

    def getAll(self):
        return (self.value, self.color)

    def show(
        self, screen: pygame.Surface, coords: tuple, bloomColor: tuple = (0, 0, 0, 0)
    ):
        if bloomColor != (0, 0, 0, 0):
            bloomSurface = pygame.Surface(
                ((self.bg.get_width() + 10), (self.bg.get_height() + 10)),
                pygame.SRCALPHA,
            )
            pygame.draw.rect(
                bloomSurface, bloomColor, bloomSurface.get_rect(), border_radius=8
            )
            screen.blit(bloomSurface, (coords[0] - 5, coords[1] - 5))
        screen.blit(self.bg, coords)


class Deck:
    def __init__(
        self,
        allCards: list[Card] = [],
        drawPile: list[Card] = [],
        onTable: list[list[Card]] = [],
        inHand: list[Card] = [],
        inOpponentHand: list[Card] = [],
        inDiscardPile: list[Card] = [],
    ):
        self.allCards: list[Card] = allCards
        self.drawPile: list[Card] = drawPile
        self.onTable: list[list[Card]] = onTable
        self.inHand: list[Card] = inHand
        self.inDiscardPile: list[Card] = inDiscardPile
        self.inOpponentHand: list[Card] = inOpponentHand
        if len(allCards) == 0:
            for i in range(2):
                for c in ["Spades", "Hearts", "Diamonds", "Clubs"]:
                    for v in range(1, 14):
                        card = Card(v, c, 0)
                        self.allCards.append(card)
                        self.drawPile.append(card)

    def pickCard(self) -> Card:
        if len(self.drawPile) == 0:
            return None
        return self.drawPile.pop()

    def playCard(self, card: Card, isPlayer: bool):
        if isPlayer:
            self.inHand.remove(card)
        else:
            self.inOpponentHand.remove(card)

    def shuffleDeck(self):
        shuffle(self.drawPile)

    def saveDeck(self) -> "Deck":
        return Deck(
            self.allCards.copy(),
            self.drawPile.copy(),
            [pile.copy() for pile in self.onTable],
            self.inHand.copy(),
            self.inOpponentHand.copy(),
            self.inDiscardPile.copy(),
        )


class cardSelected:
    def __init__(self, card: Card, come: int, y: int, x: int = 0):
        self.card = card
        self.come = come  # 0 = from hand, 1 = from table
        self.x = x  # position of list (only if come = 1)
        self.y = y  # position on list

    def selectCard(self, card: Card, come: int, y: int, x: int = 0):
        self.card = card
        self.come = come
        self.x = x
        self.y = y
