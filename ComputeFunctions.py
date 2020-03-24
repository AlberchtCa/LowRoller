import csv
import Classes
import GameFunctions
import random

def computePreflopHands(gameState):
    computed_hands = []
    r = random.SystemRandom()
    counter = 998
    counter2 = 0

    # Compute off-suit hand pairs
    # I will be using only hearts and spades
    considered_cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    considered_suits = ['h', 's']
    result = []
    for suit in considered_suits:
        for card in considered_cards:
            result.append(card + suit)

    remaining_suits = ['d', 'c']

    deck = result.copy()

    # Adding the rest of the cards to the deck
    for suit in remaining_suits:
        for card in considered_cards:
            deck.append(card + suit)

    file = open("Hands//InitialHandStrength.txt", 'a')

    for first_card in result[:-1]:
        for second_card in result[result.index(first_card)+1:]:
            current_hand = [first_card, second_card]
            current_deck = deck.copy()
            current_deck.remove(current_hand[0])
            current_deck.remove(current_hand[1])
            opponent_hand = []
            opponent_hand.append(current_deck[r.randint(0, len(current_deck) - 1)])
            current_deck.remove(opponent_hand[0])
            opponent_hand.append(current_deck[r.randint(0, len(current_deck) - 1)])
            current_deck.remove(opponent_hand[1])

            win = tie = loss = 0

            for i in range(1000):
                if counter < i:
                    print("Computed " + str(counter2 + 1) + " card(s)")
                    counter2 += 1
                felt = []
                testing_deck = current_deck.copy()
                win = tie = loss = 0
                for j in range(5):
                    felt.append(testing_deck[r.randint(0, len(testing_deck) - 1)])
                    testing_deck.remove(felt[j])

                decision = GameFunctions.decideWinningHand(current_hand, opponent_hand, felt)

                if decision == 0:
                    tie += 1
                elif decision == 1:
                    win += 1
                elif decision == 2:
                    loss += 1

            if current_hand[0][1] == current_hand[1][1]:
                offsuit = "1"
            else:
                offsuit = "0"

            file.write(','.join([current_hand[0][0], current_hand[1][0], offsuit, str(win - loss)]))
            file.write('\n')

    file.close()









#gameState = Classes.GameState()
#gameState = GameFunctions.initiateGame(gameState)
#computePreflopHands(gameState)