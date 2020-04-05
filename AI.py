import Classes
import GameFunctions
import Main
from keras.models import load_model
from keras.models import Sequential
from keras.layers import Dense, Activation


#Prima iteratie a modelului:
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

def saveModel(model,path):
    model.save('Models/'+path+'.h5')

def loadModel(path):
    bot = load_model('Models/'+path+'.h5')

initiateModel()