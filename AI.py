import Classes
import GameFunctions
import Main
from tensorflow import keras


def learnOpponent(gameState):
    pass


def handStrength(gameState):
    if gameState.player1.isAI:
        bot = gameState.player1
    else:
        bot = gameState.player2

    ahead = tied = behind = 0




