from Cards import Card, Deck

def playTurn(deck: Deck) -> Deck:
    drawCard = None
    if len(deck.inDiscardPile) > 0:
        deck.inOpponentHand.append(deck.inDiscardPile.pop())
    deck = DropTripleCard(deck)
    deck = DropLess(deck)
    deck = TreeFinding(deck)
    for card in deck.inOpponentHand:
        if drawCard != None and card == drawCard:
            pass
    return deck

def DropTripleCard(deck: Deck) -> Deck:
    isCorect = False
    # LES CARRES

    deck.inOpponentHand.sort(key=lambda card: card.value)
    cards = []
    lastValue = 0
    print("Caards: ", [card.getAll() for card in deck.inOpponentHand])
    for card in deck.inOpponentHand:
        if lastValue != card.value:
            lastValue = card.value
        hasFound = False
        for i in range(len(cards)):
            if cards[i][0].value == lastValue:
                hasFound = True
                cards[i].append(card)
        if not hasFound:
            cards.append([card])
    for cardNumber in cards:
        print([card.getAll() for card in cardNumber])
        newListe = list(set(card for card in cardNumber))
        print("ok", len(newListe))
    pass

def DropLess(deck: Deck) -> Deck:
    return deck

def TreeFinding(deck: Deck) -> Deck:
    return deck


test_deck = Deck()
test_deck.drawPile.sort(key=lambda card: card.value)
for i in range(13):
    test_deck.inOpponentHand.append(test_deck.pickCard())
playTurn(test_deck)