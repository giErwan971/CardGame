from Cards import Card, Deck


def playTurn(deck: Deck) -> list[Card]:
    drawCard = None
    drawScore = 0
    if len(deck.inDiscardPile) > 0:
        drawScore = evaluateCardPlacement(deck, deck.inDiscardPile[-1])
    moy = 0
    for card in deck.drawPile:
        score = evaluateCardPlacement(deck, card)
        moy += score
    for card in deck.inHand:
        score = evaluateCardPlacement(deck, card)
        moy += score
    moy = moy / (len(deck.drawPile) + len(deck.inHand))
    if drawScore > moy:
        drawCard = deck.inDiscardPile.pop()
        deck.inOpponentHand.append(drawCard)
    else:
        drawCard = deck.pickCard()
        deck.inOpponentHand.append(drawCard)
    deck = DropTripleCard(deck)
    deck = DropLess(deck)
    if drawCard in deck.inOpponentHand:
        deck.inOpponentHand.remove(drawCard)
        deck.inDiscardPile.append(drawCard)


    # selectedCard = DropLess(deck)
    # selectedCard = TreeFinding(deck)
    # for card in deck.inOpponentHand:
    #     if drawCard is None and card == drawCard:
    #         pass
    return deck


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


def polyvalenceCombinatoire(deck: Deck, checkCard: Card):
    compSuite = [checkCard]
    cartes_proches = 0      # Cartes à ±1 ou ±2
    cartes_moyennes = 0     # Cartes à ±3 à ±5
    cartes_lointaines = 0   # Cartes à ±6+
    
    for card in deck.inOpponentHand:
        if card.color == checkCard.color and card.value != checkCard.value:
            distance = abs(card.value - checkCard.value)
            
            if distance <= 2:
                cartes_proches += 1
                compSuite.append(card)
            elif distance <= 5:
                cartes_moyennes += 1
                compSuite.append(card)
            elif distance <= 10:
                cartes_lointaines += 1
                compSuite.append(card)

    # RÉAJUSTEMENT : favoriser les suites polyvalentes
    score_suite = cartes_proches * 18
    score_suite += cartes_moyennes * 8
    score_suite += cartes_lointaines * 3
    print(f"Polyvalence suite score: {score_suite}")
    
    compGroup = [checkCard]
    for card in deck.inOpponentHand:
        if card.value == checkCard.value and card.color != checkCard.color:
            compGroup.append(card)
    score_group = (len(compGroup)-1) * 12
    print(f"Polyvalence group score: {score_group}")
    
    # Max 40 points pour polyvalence (ce n'est qu'une composante)
    score_polyvalence = min(score_suite + score_group, 40)
    print(f"Total polyvalence score: {score_polyvalence}")
    
    return (score_polyvalence, compSuite, compGroup)


def positionDansSequence(deck: Deck, checkCard: Card, compSuite, compGroup):
    compSuite.sort(key=lambda x: x.value)
    
    # Si groupe complet = très bon
    if len(compGroup) == 3:
        return 20  # Hausse de 10 à 20
    
    if len(compSuite) >= 3:
        if checkCard != compSuite[0] and checkCard != compSuite[-1]:
            return 15  # Position INTERNE (hausse)
    return 0


def checkDoublon(deck: Deck, checkCard: Card):
    for card in deck.inOpponentHand:
        if card.value == checkCard.value and card.color == checkCard.color:
            return -25  # Pénalité plus forte
    return 0


def nbPose(deck: Deck, checkCard: Card):
    """
    Simule l'impact de cette carte sur le nombre de poses possibles.
    Plus on peut poser de cartes, mieux c'est.
    """
    newDeck = Deck(
        allCards=deck.allCards.copy(),
        drawPile=deck.drawPile.copy(),
        onTable=deck.onTable.copy(),
        inHand=deck.inHand.copy(),
        inOpponentHand=deck.inOpponentHand.copy(),
        inDiscardPile=deck.inDiscardPile.copy())
    
    start = len(newDeck.inOpponentHand)
    newDeck = playTurn(newDeck)
    end = len(newDeck.inOpponentHand)
    score1 = start - end
    
    newDeck = Deck(
        allCards=deck.allCards.copy(),
        drawPile=deck.drawPile.copy(),
        onTable=deck.onTable.copy(),
        inHand=deck.inHand.copy(),
        inOpponentHand=deck.inOpponentHand.copy(),
        inDiscardPile=deck.inDiscardPile.copy())
    newDeck.inOpponentHand.append(newDeck.inDiscardPile.pop())
    start = len(newDeck.inOpponentHand)
    newDeck = playTurn(newDeck)
    end = len(newDeck.inOpponentHand)
    score2 = start - end
    
    difference = (score1 - score2) + 1
    print(f"NbPose difference: {difference}")
    
    # RÉAJUSTEMENT : bonus jusqu'à 25 max pour nbPose
    return min(difference * 6, 25), difference


def evaluateCardPlacement(deck: Deck, checkCard: Card):
    """
    Évaluation totale : 0-100
    0 = inutile
    50 = peut servir plus tard
    100 = victoire quasi assurée
    """
    totalScore = 0
    
    # Composante 1 : Polyvalence (0-40)
    polyvalenceScore, compSuite, compGroup = polyvalenceCombinatoire(deck, checkCard)
    totalScore += polyvalenceScore
    
    # Composante 2 : Position (0-20)
    positionScore = positionDansSequence(deck, checkCard, compSuite, compGroup)
    print(f"Position score: {positionScore}")
    totalScore += positionScore
    
    # Composante 3 : Doublon (-25 à 0)
    doublonScore = checkDoublon(deck, checkCard)
    print(f"Doublon score: {doublonScore}")
    totalScore += doublonScore
    
    # Composante 4 : Impact pose (0 à +25)
    #poseScore, diff = nbPose(deck, checkCard)
    #print(f"Pose score: {poseScore}")
    #totalScore += poseScore
    
    # NORMALISATION : ramener entre 0 et 100
    # Minimum possible : -25 = -25 → devient 0
    # Maximum possible : 40 + 20 + 25 = 85 → devient 100
    totalScore = round((totalScore+25)/110 * 100, 2)
    
    return totalScore


def Test():
    deck = Deck()
    deck.shuffleDeck()
    deck.inOpponentHand = [deck.pickCard() for _ in range(7)]
    deck.inDiscardPile = [deck.pickCard() for _ in range(1)]
    moy = 0
    moy2 =0
    for card in deck.drawPile:
        score = evaluateCardPlacement(deck, card)
        moy += score
    print(f"Average score: {moy / len(deck.drawPile)}")



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
    #Test()
