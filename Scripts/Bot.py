import Cards
def playTurn(deck: Cards.Deck) -> Cards.Deck:
    drawCard = deck.inOpponentHand.append(deck.discardPile.pop())
    deck = DropTripleCard(deck)
    deck = DropLess(deck)
    deck = TreeFinding(deck)
    for card in deck.inOpponentHand:
        if card == drawCard:
            pass
    return deck

def DropTripleCard(deck: Cards.Deck) -> Cards.Deck:
    pass

def DropLess(deck: Cards.Deck) -> Cards.Deck:
    pass

def TreeFinding(deck: Cards.Deck) -> Cards.Deck:
    pass