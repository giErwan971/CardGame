from random import *
import pygame
class Card:
    def __init__(self, value, color, etat):
        self.value = value
        self.color = color
        self.etat = etat #0 = in draw pile, 1 = in hand, 2 = in opponent hand, 3 = on table
        self.bg = pygame.image.load(f"Assets\\Cards\\King's Cards\\Suit Of {color}\\{color}_{value}.png")
    def getAll(self):
        return(self.value, self.color)
    def show(self, screen : pygame.Surface, coords: tuple, bloom: bool = False):
        if bloom:
            bloomSurface = pygame.Surface((self.bg.get_width()+10, self.bg.get_height()+10), pygame.SRCALPHA)
            pygame.draw.rect(bloomSurface, (0, 150, 255, 100), bloomSurface.get_rect(), border_radius=8)
            screen.blit(bloomSurface, (coords[0]-5, coords[1]-5))
        screen.blit(self.bg, coords)

class Deck:
    def __init__(self):
        self.allCards: list[Card] = []
        self.drawPile: list[Card] = []
        self.onTable: list[list[Card]] = []
        self.inHand: list[Card] = []
        self.inOpponentHand: list[Card] = []
        self.inOpponentHand: list[Card] = []
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
    