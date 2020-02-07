import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense  # Dropout, Activation, LSTM
from keras.models import model_from_json
from sklearn.metrics import mean_squared_error
import math
import datetime
# other modules:
# from keras.optimizers import SGD
# from sklearn.preprocessing import MinMaxScaler
# import sys
# import keras
# import configparser
# import numpy as np


def train_model_dnn(trainX, trainY, epoch=1, btsize=1):
    """
    use input training X and Y to make a model
    trainX and trainY are np.array
    """
    print(datetime.datetime.now(),
          "trainX shape: ", trainX.shape,
          "trainY shape: ", trainY.shape)
    dimX = trainX.shape[1]  # number of X points used to predict Y
    # trainX = trainX.reshape(trainX.shape[0], 1, trainX.shape[1])
    # trainY = trainY.reshape(trainY.shape[0], 1)

    model = Sequential()
    # model.add(Dense(128, activation='relu', input_shape=(1, dimX)))
    model.add(Dense(128, input_dim=dimX, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(10, activation='relu'))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(trainX, trainY, epochs=epoch, batch_size=btsize, verbose=2)

    print(datetime.datetime.now(), " fit training model.")
    trainPredict = model.predict(trainX)

    print(datetime.datetime.now(), "trainY shape: ", trainY.shape)
    print(datetime.datetime.now(), "trainP shape: ", trainPredict.shape)
    print(datetime.datetime.now(), " save training model.")

    # serialize model to JSON
    model_json = model.to_json()
    with open("model_dnn.json", "w") as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    model.save_weights("model_dnn.h5")

    # calculate root mean squared error
    trainScore = math.sqrt(mean_squared_error(trainY, trainPredict))
    print(datetime.datetime.now(), 'Train Score: %.5f RMSE' % (trainScore))

    plt.plot(range(0, len(trainY)), trainY, c="darkred")
    plt.plot(range(0, len(trainY)), trainPredict, c="mediumseagreen")
    plt.title("Prediction vs measured")
    plt.xlabel("Index")
    plt.ylabel("Time to quake (ms)")
    plt.savefig('train_'+str(datetime.datetime.now())+'.png')
    return model


def load_model_dnn(jsmodelname="model_dnn.json", weightname="model_dnn.h5"):
    """
    load json and create model
    """
    json_file = open(jsmodelname, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights(weightname)
    print("Loaded model from disk")
    return loaded_model
