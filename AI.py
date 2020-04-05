import csv
from keras.models import load_model
from keras.models import Sequential
from keras.layers import Dense


# Prima iteratie a modelului:
def initiateModel():
    player1 = Sequential()
    player1.add(Dense(10, activation='relu',kernel_initializer='random_normal'))
    player1.add(Dense(15, activation='relu',kernel_initializer='random_normal'))
    player1.add(Dense(3, activation='softmax',kernel_initializer='random_normal'))
    player1.compile(optimizer='SGD',
                    loss='mean_squared_error',
                    metrics='accuracy')
    player2 = Sequential()
    player2.add(Dense(10, activation='relu',kernel_initializer='random_normal'))
    player2.add(Dense(15, activation='relu',kernel_initializer='random_normal'))
    player2.add(Dense(3, activation='softmax',kernel_initializer='random_normal'))
    player2.compile(optimizer='SGD',
                    loss='mean_squared_error',
                    metrics='accuracy')

    return player1, player2


# La urmatoarele iteratii, il salvez si il incarc pe modelul cel mai avansat pentru a juca
# impotriva lui cu scopul dezvoltarii
def saveModel(model, path, data):
    model.save('Models/'+path+'.h5')
    with open('OppData/Model' + model + '_data.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for i in range(13):
            for j in range(13):
                writer.writerow([i] + [j] + [data[i][j]])

def loadModel(path):
    bot = load_model('Models/'+path+'.h5')
    return bot

def trainAI(model):
    pass

# Calculeaza indexul mainii personale


# Calculez mana pe care o are in momentul de fata AI-ul
#def computeIndex(hand, felt):
#    total = felt + hand
#    if len(total) == 5:
#        return GameFunctions.getHandIndex(total)
#    else:
#        getBestHandIndex(total)

