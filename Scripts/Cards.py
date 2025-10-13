from random import *
class Card:
    def __init__(self, value, color):
        self.value = value
        self.color = color
    def getAll(self):
        return(self.value, self.color)

class Deck:
    def __init__(self):
        self.allCards = []
        for c in ["Spades", "Hearts", "Diamonds", "Clubs"]:
            for v in range(1, 14):
                self.allCards.append(Card(v, c))

    def pickCard(self):
        return self.allCards.pop()
    
    def shuffleDeck(self):
        shuffle(self.allCards)
        

deck = Deck()
deck.shuffleDeck()
    