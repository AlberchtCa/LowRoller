import random
import itertools
import AI_Playing

### INITIATION FUNCTIONS ###
def initiateGame(gameState):
    cards = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
    suits = ['h', 'c', 's', 'd']
    deck = []
    for i in range(13):
        for j in range(4):
            deck.append(cards[i] + suits[j])
    gameState.cards = deck.copy()
    gameState.player1.cards = []
    gameState.player1.cards = []
    gameState.player2.cards = []
    gameState.felt = []
    gameState.actions = []
    gameState.pot = 0
    gameState.last_action = "None"
    gameState.round_done = False
    gameState.game_done = False
    return gameState


### START GAME ###
def startGame(gameState):
    gameState = initiateGame(gameState)
    gameState = dealCards(gameState)
    showCards(gameState)
    gameState = playPreflop(gameState)
    if not gameState.game_done:
        gameState = getFlop(gameState)
        showFelt(gameState)
        gameState = playRound(gameState)
    if not gameState.game_done:
        gameState = getTurn(gameState)
        showFelt(gameState)
        gameState = playRound(gameState)
    if not gameState.game_done:
        gameState = getRiver(gameState)
        showFelt(gameState)
        gameState = playRound(gameState)
    if not gameState.game_done:
        winner = decideWinningHand(gameState.player1.cards, gameState.player2.cards, gameState.felt)
        if winner == 0:
            pass
        else:
            if winner == 1:
                gameState.player1.blinds += gameState.pot
                gameState.pot = 0
            else:
                if winner == 2:
                    gameState.player2.blinds += gameState.pot
                    gameState.pot = 0
    return gameState


def showCards(gameState):
    print("Player 1 has: ")
    for card in gameState.player1.cards:
        print(card)
    print("Player 2 has: ")
    for card in gameState.player2.cards:
        print(card)

def showFelt(gameState):
    for card in gameState.felt:
        print(card)

def showToAct(gameState):
    if gameState.player1.hasAction:
        print("Player 1 is to act. \n")
    else:
        print("Player 2 is to act. \n")


def dealCards(gameState):
    gameState.player1.cards.append(gameState.cards[random.randint(0, len(gameState.cards) - 1)])
    gameState.cards.remove(gameState.player1.cards[0])
    gameState.player1.cards.append(gameState.cards[random.randint(0, len(gameState.cards) - 1)])
    gameState.cards.remove(gameState.player1.cards[1])

    gameState.player2.cards.append(gameState.cards[random.randint(0, len(gameState.cards) - 1)])
    gameState.cards.remove(gameState.player2.cards[0])
    gameState.player2.cards.append(gameState.cards[random.randint(0, len(gameState.cards) - 1)])
    gameState.cards.remove(gameState.player2.cards[1])

    gameState.street = 'preflop'
    return gameState

def playPreflop(gameState):
    gameState.round_done = False
    gameState.street = 'preflop'
    if gameState.player1.isButton:
        gameState.player1.hasAction = True
        gameState.player2.blinds -= 1
        gameState.pot += 1
    else:
        gameState.player2.hasAction = True
        gameState.player1.blinds -= 1
        gameState.pot += 1
    gameState = getBlinds(gameState)
    while gameState.round_done is False:
        showToAct(gameState)
        showOptions(gameState)
        gameState = chooseAction(gameState)
        gameState = switchAction(gameState)
    return gameState

def playRound(gameState):
    gameState.round_done = False
    if gameState.player1.isButton:
        gameState.player2.hasAction = True
    else:
        gameState.player2.hasAction = True
    while gameState.round_done is False:
        showToAct(gameState)
        showOptions(gameState)
        gameState = chooseAction(gameState)
        gameState = switchAction(gameState)
    return gameState

def chooseAction(gameState):
    acting_player = getActingPlayer(gameState)
    unacting_player = getUnactingPlayer(gameState)
    if not acting_player.isAI:
        chosen_action = int(input())
    else:
        chosen_action = AI_Playing.decide_action(gameState)

    if gameState.last_action == "None" and gameState.street == 'preflop':
        if chosen_action == 1:
            gameState.last_action = "None"
            gameState.round_done = True
            gameState.game_done = True
            unacting_player.blinds += gameState.pot
        if chosen_action == 2:
            gameState.last_action = "Call"
            acting_player.blinds -= 1
            gameState.pot += 1
        if chosen_action == 3:
            acting_player.blinds -= 2
            gameState.pot += 2
            gameState.last_action = "Raise"
    else:
        if gameState.last_action == "None":
            if chosen_action == 1:
                gameState.last_action = "Check"
            if chosen_action == 2:
                acting_player.blinds -= 1
                gameState.pot += 1
                gameState.last_action = "Bet"
        else:
            if gameState.last_action == "Bet":
                if chosen_action == 1:
                    gameState.last_action = "None"
                    gameState.round_done = True
                    gameState.game_done = True
                    unacting_player.blinds += gameState.pot
                if chosen_action == 2:
                    gameState.last_action = "None"
                    gameState.round_done = True
                    acting_player.blinds -= 1
                    gameState.pot += 1
                if chosen_action == 3:
                    gameState.last_action = "Raise"
                    acting_player.blinds -= 1
                    gameState.pot += 1
            else:
                if gameState.last_action == "Raise":
                    if chosen_action == 1:
                        gameState.last_action = "None"
                        gameState.round_done = True
                        gameState.game_done = True
                        unacting_player.blinds += gameState.pot

                    if chosen_action == 2:
                        gameState.last_action = "None"
                        gameState.round_done = True
                        acting_player.blinds -= 1
                        gameState.pot += 1
                else:
                    if gameState.last_action == "Check":
                        if chosen_action == 1:
                            gameState.last_action = "None"
                            gameState.round_done = True
                        if chosen_action == 2:
                            gameState.last_action = "Bet"
                            acting_player.blinds -= 1
                            gameState.pot += 1
                    else:
                        if gameState.last_action == "Call":
                            if chosen_action == 1:
                                gameState.last_action = "None"
                                gameState.round_done = True
                            if chosen_action == 2:
                                gameState.last_action = "Bet"
                                acting_player.blinds -= 1
                                gameState.pot += 1

    if gameState.player1.hasAction:
        gameState.player1 = acting_player
        gameState.player2 = unacting_player
    else:
        gameState.player2 = acting_player
        gameState.player1 = unacting_player
    return gameState



def getActingPlayer(gameState):
    if gameState.player1.hasAction:
        return gameState.player1
    else:
        return gameState.player2

def getUnactingPlayer(gameState):
    if gameState.player1.hasAction:
        return gameState.player2
    else:
        return gameState.player1

def getBlinds(gameState):
    if gameState.player1.isButton:
        gameState.player1.blinds -= 1
        gameState.pot = 1
    return gameState


def showOptions(gameState):
    if gameState.last_action == "None" and gameState.street == 'preflop':
        print("1. Fold \n2. Call\n3. Raise")
    else:
        if gameState.last_action == "None":
            print("\n1. Check\n2. Bet")
        else:
            if gameState.last_action == "Bet":
                print("1. Fold\n2. Call\n3.Raise")
            else:
                if gameState.last_action == "Raise":
                    print("1.Fold\n2.Call")
                else:
                    if gameState.last_action == "Check":
                        print("1.Check\n2.Bet")
                    else:
                        if gameState.last_action == "Call":
                            print("1.Check\n2.Bet")



def switchAction(gameState):
    if gameState.player1.hasAction:
        gameState.player2.hasAction = True
        gameState.player1.hasAction = False
    else:
        gameState.player1.hasAction = True
        gameState.player2.hasAction = False
    return gameState


def getCardOnFelt(gameState):
    gameState.felt.append(gameState.cards[random.randint(0, len(gameState.cards) -1)])
    gameState.cards.remove(gameState.felt[len(gameState.felt) - 1])
    return gameState


def getFlop(gameState):
    for i in range(3):
        gameState = getCardOnFelt(gameState)
    gameState.street = 'flop'
    return gameState


def getTurn(gameState):
    gameState = getCardOnFelt(gameState)
    gameState.street = 'turn'
    return gameState


def getRiver(gameState):
    gameState = getCardOnFelt(gameState)
    gameState.street = 'river'
    return gameState


def decideWinningHand(gameState):
    felt1 = []
    felt2 = []
    for i in range(5):
        felt1.append(gameState.felt[i])
        felt2.append(gameState.felt[i])
    for i in range(2):
        felt1.append(gameState.player1.cards[i])
        felt2.append(gameState.player2.cards[i])

    combos = list(itertools.combinations([0, 1, 2, 3, 4, 5, 6], 5))

    bestHandInit1 = []
    for i in range(5):
        bestHandInit1.append(felt1[i])

    bestHandInit2 = []
    for i in range(5):
        bestHandInit2.append(felt2[i])

    for i in range(21):
        if i == 0:
            pass
        bestHandContender = []
        for j in range(5):
            bestHandContender.append(felt1[combos[i][j]])

        winningHand = getBetterHand(bestHandInit1, bestHandContender)
        if(winningHand != 0):
            bestHandInit1 = winningHand
        else:
            pass

    for i in range(21):
        if i == 0:
            pass
        bestHandInitTemp = []
        bestHandContender = []
        for j in range(5):
            bestHandContender.append(felt2[combos[i][j]])

        winningHand = getBetterHand(bestHandInit2, bestHandContender)
        if winningHand != 0:
           bestHandInit2 = winningHand
        else:
           pass

    bestHand = getBetterHand(bestHandInit1, bestHandInit2)

    print("Player 1 has:")
    print(bestHandInit1)

    print("Player 2 has:")
    print(bestHandInit2)

    if bestHand == 0:
        print("Draw:")
        print(bestHandInit1)
        print(bestHandInit2)
        gameState.player1.blinds += gameState.pot / 2
        gameState.player2.blinds += gameState.pot / 2
    if bestHand == bestHandInit1:
        print("Player 1 wins with:")
        print(bestHandInit1)
        gameState.player1.blinds += gameState.pot
    else:
        if bestHand == bestHandInit2:
            print("Player 2 wins with:")
            print(bestHandInit2)
            gameState.player2.blinds += gameState.pot
    return gameState



def countCards(hand):
    cards = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for i in range(5):
        for j in range(14):
            if hand[i][0] == cards[j]:
                count[j] += 1
    return count


def isStraightFlush(hand):
    if isStraight(hand) and isFlush(hand):
        return True
    return False


def isStraight(hand):
    count = countCards(hand)
    chinta = 0
    for i in range(13):
        if count[i] == count[i + 1] and count[i] == 1:
            chinta += 1

    if chinta == 4:
        return True
    else:
        return False


def isFlush(hand):
    suits = ['s', 'c', 'h', 'd']
    count = [0, 0, 0, 0]
    for i in range(5):
        for j in range(4):
            if suits[j] == hand[i][1]:
                count[j] += 1
    for i in range(4):
        if count[i] == 5:
            return True
    return False


def isFourOfAKind(hand):
    count = countCards(hand)
    for i in range(13):
        if count[i] == 4:
            return True
    return False


def isPair(hand):
    count = countCards(hand)
    maxim = 0
    for i in range(13):
        if count[i] == 2:
            maxim += 1
    if maxim == 1:
        return True
    return False


def isTwoPair(hand):
    count = countCards(hand)
    maxim = 0
    for i in range(13):
        if count[i] == 2:
            maxim += 1
    if maxim == 2:
        return True
    return False


def isThreeOfAKind(hand):
    count = countCards(hand)
    for i in range(13):
        if count[i] == 3:
            return True
    return False


def isFullHouse(hand):
    if isPair(hand) and isThreeOfAKind(hand):
        return True
    return False


def getHandIndex(hand):
    index = 0
    # High Card = 0
    # Pair      = 1
    # Two Pair  = 2
    # 3OAK      = 3
    # Straight  = 4
    # Flush     = 5
    # Full House= 6
    # 4OAK      = 7
    # Str. Flsh = 8

    if isPair(hand):
        index = 1
    if isTwoPair(hand):
        index = 2
    if isThreeOfAKind(hand):
        index = 3
    if isStraight(hand):
        index = 4
    if isFlush(hand):
        index = 5
    if isFullHouse(hand):
        index = 6
    if isFourOfAKind(hand):
        index = 7
    if isStraightFlush(hand):
        index = 8

    return index


def getBetterHand(hand1, hand2):
    index1 = getHandIndex(hand1)
    index2 = getHandIndex(hand2)
    # High Card = 0
    # Pair      = 1
    # Two Pair  = 2
    # 3OAK      = 3
    # Straight  = 4
    # Flush     = 5
    # Full House= 6
    # 4OAK      = 7
    # Str. Flsh = 8

    if (index1 == index2) and (index1 != 6):
        count1 = countCards(hand1)
        count2 = countCards(hand2)
        i = 13
        while count1[i] == count2[i] and i >= 0:
            i -= 1
        if i == -1:
            return 0
        else:
            if count1[i] != 0:
                return hand1
            else:
                return hand2

    if (index1 == index2) and (index1 == 6):
        count1 = countCards(hand1)
        count2 = countCards(hand2)
        i = 13
        while count1[i] == count2[i] and i >= 0:
            i -= 1
        if i == -1:
            return 0
        else:
            if count1[i] == 3:
                return hand1
            else:
                if count2[i] == 3:
                    return hand2
                else:
                    if count1[i] == 2:
                        return hand1
                    else:
                        return hand2

    else:
        if index1 > index2:
            return hand1
        else:
            return hand2

def getBetterHandIndex(hand1, hand2):
    index1 = getHandIndex(hand1)
    index2 = getHandIndex(hand2)
    # High Card = 0
    # Pair      = 1
    # Two Pair  = 2
    # 3OAK      = 3
    # Straight  = 4
    # Flush     = 5
    # Full House= 6
    # 4OAK      = 7
    # Str. Flsh = 8

    if (index1 == index2) and (index1 != 6):
        count1 = countCards(hand1)
        count2 = countCards(hand2)
        i = 13
        while count1[i] == count2[i] and i >= 0:
            i -= 1
        if i == -1:
            return 0
        else:
            if count1[i] != 0:
                return hand1
            else:
                return hand2

    if (index1 == index2) and (index1 == 6):
        count1 = countCards(hand1)
        count2 = countCards(hand2)
        i = 13
        while count1[i] == count2[i] and i >= 0:
            i -= 1
        if i == -1:
            return 0
        else:
            if count1[i] == 3:
                return hand1
            else:
                if count2[i] == 3:
                    return hand2
                else:
                    if count1[i] == 2:
                        return hand1
                    else:
                        return hand2

    else:
        if index1 > index2:
            return index1
        else:
            return index2

def decideWinningHand(hand1, hand2, felt):
    felt1 = []
    felt2 = []
    for i in range(5):
        felt1.append(felt[i])
        felt2.append(felt[i])
    for i in range(2):
        felt1.append(hand1[i])
        felt2.append(hand2[i])

    combos = list(itertools.combinations([0, 1, 2, 3, 4, 5, 6], 5))

    bestHandInit1 = []
    for i in range(5):
        bestHandInit1.append(felt1[i])

    bestHandInit2 = []
    for i in range(5):
        bestHandInit2.append(felt2[i])

    for i in range(21):
        if i == 0:
            pass
        bestHandContender = []
        for j in range(5):
            bestHandContender.append(felt1[combos[i][j]])

        winningHand = getBetterHand(bestHandInit1, bestHandContender)
        if (winningHand != 0):
            bestHandInit1 = winningHand
        else:
            pass

    for i in range(21):
        if i == 0:
            pass
        bestHandInitTemp = []
        bestHandContender = []
        for j in range(5):
            bestHandContender.append(felt2[combos[i][j]])

        winningHand = getBetterHand(bestHandInit2, bestHandContender)
        if winningHand != 0:
            bestHandInit2 = winningHand
        else:
            pass

    bestHand = getBetterHand(bestHandInit1, bestHandInit2)

    if bestHand == 0:
        return 0
    if bestHand == bestHandInit1:
        return 1
    else:
        return 2

def getBestHandIndex(hand, felt):
    total = hand + felt
    util_vect = []
    for i in range(len(total)):
        util_vect.append(i)
    combos = list(itertools.combinations(util_vect, 5))
    if len(felt) == 3:
        return getHandIndex(total)

    initial_hand = []
    for i in range(5):
        initial_hand.append(total[i])

    if len(felt) == 4:
        target = 6
    if len(felt) == 5:
        target = 21
    for i in range(target):
        if i == 0:
            pass
        bestHandContender = []
        for j in range(5):
            bestHandContender.append(total[combos[i][j]])
        winningHand = getBetterHand(initial_hand, bestHandContender)
        if (winningHand != 0):
            initial_hand = winningHand
        else:
            pass

    return getHandIndex(initial_hand)