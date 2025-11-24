from Cards import Card, Deck


def playTurn(deck: Deck) -> list[Card]:
    drawCard = None
    if len(deck.inDiscardPile) > 0:
        deck.inOpponentHand.append(deck.inDiscardPile.pop())
    selectedCard = []
    selectedCard = DropTripleCard(deck)

    print("Selected Cards:")
    [print(card.getAll()) for card in selectedCard]

    # selectedCard = DropLess(deck)
    # selectedCard = TreeFinding(deck)
    # for card in deck.inOpponentHand:
    #     if drawCard is None and card == drawCard:
    #         pass
    return selectedCard


def DropTripleCard(deck: Deck) -> list[Card]:
    # LES CARRES

    deck.inOpponentHand.sort(key=lambda card: card.value)
    cards: list[list[Card]] = []
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
        if len(cardNumber) >= 3:
            return cardNumber

    # SUITE

    cards.clear()
    for card in deck.inOpponentHand:
        if len(cards) == 0:
            cards.append([card])
            # cards[0].append(card)
            continue
        isValid = False
        for cardList in cards:
            if cardList[0].color == card.color:
                cardList.append(card)
                isValid = True
                break
        if not isValid:
            cards.append([card])
    for cardList in cards:
        cardList.sort(key=lambda card: card.value)
        suiteCards: list[Card] = []
        suiteCount = 0
        lastValue = 0
        for card in cardList:
            if lastValue == 0:
                lastValue = card.value
                suiteCount = 1
                suiteCards.append(card)
            elif lastValue == card.value - 1:
                suiteCount += 1
                suiteCards.append(card)
                lastValue = card.value
            else:
                suiteCount = 0
                lastValue = 0
                suiteCards.clear()
        if suiteCount >= 3:
            return suiteCards
    return []


def DropLess(deck: Deck) -> Deck:
    return deck


def TreeFinding(deck: Deck) -> Deck:
    return deck



if __name__ == "__main__":
    test_deck = Deck()
    test_deck.shuffleDeck()
    # test_deck.drawPile.sort(key=lambda card: card.value)
    for i in range(10):
        # test_card = Card(i + 1, "Spades", 0)
        # test_deck.inOpponentHand.append(test_card)
        test_deck.inOpponentHand.append(test_deck.pickCard())
    playTurn(test_deck)
