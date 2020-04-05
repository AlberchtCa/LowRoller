import GameFunctions
import Classes
import AI

#gameState = GameFunctions.startGame(gameState)

#print(gameState.player1.cards[0])
#print(gameState.player1.cards[1])
#print(gameState.player2.cards[0])
#print(gameState.player2.cards[1])

testHand = ['2c', '3d', '4c', '5h', '6s']
testHand2 = ['Ts', 'Jc', 'Qs', 'Kh', 'As']
testHand3 = ['2d', '3d', '4d', '5d', 'Ad']
testHand4 = ['Ac', 'As', 'Ad', 'Ah', '2s']

def game_loop():
    gameState = Classes.GameState()
    decision = 1

    player1, player2 = AI.initiateModel()

    while decision != 0:
        print('0. Exit')
        print('1. Make AI play hands')
        print('2. Show AI blinds')
        print('3. Train AI')
        print('4. Save AI')
        decision = int(input())
        if decision == 0:
            pass

        if decision == 1:
            print('How many hands?')
            decision2 = int(input())
            for i in range(decision2):
                gameState = GameFunctions.initiateGame(gameState)
                gameState = GameFunctions.startGame(gameState)

        if decision == 2:
            print(gameState.player1.blinds)

        if decision == 3:
            AI.trainAI(player1)

        if decision == 4:
            oppData = ['nada']
            AI.saveModel(player1, 'Alfa0', oppData)

game_loop()