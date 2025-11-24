from Cards import Card, Deck


def playTurn(deck: Deck) -> list[Card]:
    drawCard = None
    if len(deck.inDiscardPile) > 0:
        deck.inOpponentHand.append(deck.inDiscardPile.pop())
    selectedCard = []
    deck = DropTripleCard(deck)

    print("Selected Cards:")
    [print(card.getAll()) for card in selectedCard]

    # selectedCard = DropLess(deck)
    # selectedCard = TreeFinding(deck)
    # for card in deck.inOpponentHand:
    #     if drawCard is None and card == drawCard:
    #         pass
    return selectedCard


def DropTripleCard(deck: Deck) -> Deck:
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
            deck.onTable.append(cardNumber)
            return deck
            # return cardNumber

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
            deck.onTable.append(suiteCards)
            return deck
    return deck


def DropLess(deck: Deck) -> Deck:
    deck.inOpponentHand.sort(key=lambda card: card.value)

    for cardCombinaison in deck.onTable:
        # Vérifie si c'est une suite ou non
        if len(cardCombinaison) < 2:
            continue
        if cardCombinaison[0].value == cardCombinaison[1].value:
            cards: list[Card] = []
            for card in deck.inOpponentHand:
                if card.value == cardCombinaison[0].value:
                    cards.append(card)
            if len(cards) > 0:
                [cardCombinaison.append(card) for card in cards]
                return deck
        else:
            lastCardSuite = cardCombinaison[len(cardCombinaison) - 1]
            cards: list[Card] = []
            for card in deck.inOpponentHand:
                if lastCardSuite.color != card.color:
                    continue
                if len(cards) == 0:
                    if lastCardSuite.value != card.value - 1:
                        continue
                    cards.append(card)
                if cards[len(cards) - 1].value == card.value - 1:
                    cards.append(card)
            if len(cards) > 0:
                [cardCombinaison.append(card) for card in cards]
                return deck
    return deck


def TreeFinding(deck: Deck) -> Deck:
    return deck


if __name__ == "__main__":
    print("Bot test:")
    test_deck = Deck()
    # test_deck.shuffleDeck()
    test_deck.onTable.append([Card(2, "Spades", 0) for _ in range(2)])
    test_deck.drawPile.sort(key=lambda card: card.value)
    for i in range(2):
        test_card = Card(2, "Spades", 0)
        test_deck.inOpponentHand.append(test_card)
        # test_deck.inOpponentHand.append(test_deck.pickCard())
    # playTurn(test_deck)
    DropLess(test_deck)
