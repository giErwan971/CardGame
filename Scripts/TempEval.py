import Cards

def polyvalenceCombinatoire(deck: Cards.Deck, checkCard: Cards.Card):
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


def positionDansSequence(deck: Cards.Deck, checkCard: Cards.Card, compSuite, compGroup):
    compSuite.sort(key=lambda x: x.value)
    
    # Si groupe complet = très bon
    if len(compGroup) == 3:
        return 20  # Hausse de 10 à 20
    
    if len(compSuite) >= 3:
        if checkCard != compSuite[0] and checkCard != compSuite[-1]:
            return 15  # Position INTERNE (hausse)
    return 0


def checkDoublon(deck: Cards.Deck, checkCard: Cards.Card):
    for card in deck.inOpponentHand:
        if card.value == checkCard.value and card.color == checkCard.color:
            return -25  # Pénalité plus forte
    return 0


def nbPose(deck: Cards.Deck, checkCard: Cards.Card):
    """
    Simule l'impact de cette carte sur le nombre de poses possibles.
    Plus on peut poser de cartes, mieux c'est.
    """
    start = len(deck.inOpponentHand)
    # Simuler tour avec la carte actuelle
    end = len(deck.inOpponentHand)
    score1 = start - end
    
    newDeck = Cards.Deck(
        allCards=deck.allCards.copy(),
        drawPile=deck.drawPile.copy(),
        onTable=deck.onTable.copy(),
        inHand=deck.inHand.copy(),
        inOpponentHand=deck.inOpponentHand.copy(),
        inDiscardPile=deck.inDiscardPile.copy())
    newDeck.inOpponentHand.append(newDeck.inDiscardPile.pop())
    start = len(newDeck.inOpponentHand)
    # Simuler tour sans la carte
    end = len(newDeck.inOpponentHand)
    score2 = start - end
    
    difference = score1 - score2
    
    # RÉAJUSTEMENT : bonus jusqu'à 25 max pour nbPose
    return min(difference * 6, 25)


def evaluateCardPlacement(deck: Cards.Deck, checkCard: Cards.Card):
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
    poseScore = nbPose(deck, checkCard)
    print(f"Pose score: {poseScore}")
    totalScore += poseScore
    
    # NORMALISATION : ramener entre 0 et 100
    # Minimum possible : -25 = -25 → devient 0
    # Maximum possible : 40 + 20 + 25 = 85 → devient 100
    totalScore = round((totalScore+25)/110 * 100, 2)
    
    return totalScore


def Test():
    deck = Cards.Deck()
    deck.shuffleDeck()
    deck.inOpponentHand = [deck.pickCard() for _ in range(7)]
    deck.inDiscardPile = [deck.pickCard() for _ in range(1)]
    moy = 0
    for card in deck.drawPile:
        score = evaluateCardPlacement(deck, card)
        print([_card.getAll() for _card in deck.inOpponentHand])
        print(f"Card: {card.getAll()}, Score: {score}")
        moy += score
    print(f"Average score: {moy / len(deck.drawPile)}")
Test()