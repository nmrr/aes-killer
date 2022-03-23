"""
MIT License

Copyright (c) 2022 nmrr (https://github.com/nmrr)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import sys

## TO DISABLE CUDA ##
#os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
#os.environ.pop('TF_CONFIG', None)

import numpy as np
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from tensorflow.keras.optimizers import SGD
from tensorflow import keras
from keras import backend as K
import gc

SIZE = 32*8

trainData = np.genfromtxt("./ctr-50k.dat", delimiter=' ', dtype=int)
xData = trainData[::2]
yData = trainData[1::2]
del trainData

testData = np.loadtxt("./ctr-10k-test.dat", delimiter=' ', dtype=int)
xData_test = testData[::2]
yData_test = testData[1::2]
del testData

initial = True
epochsCounter = 0
reccord = 1.0
counterModel = 0

increment = 1
maximumEpochs = 1000
epochtest = 5

model = Sequential()
#model = keras.models.load_model('')

while True:

    if(initial == False):
        print("using same model : ", counterModel)
    else:
        counterModel += 1
        model.add(Dense(SIZE*4, input_dim=SIZE, activation='relu'))
        model.add(Dense(SIZE, activation='sigmoid'))
        initial = False
        sgd = SGD(learning_rate=0.01)
        model.compile(loss='binary_crossentropy', optimizer='sgd')
        print("model : ", counterModel)


    model.fit(xData, yData, epochs=increment+epochsCounter, batch_size=1, initial_epoch=epochsCounter, shuffle=True)
    epochsCounter += increment

    model.save('./ctr-tmp.h5')

    K.clear_session()
    gc.collect()

    if epochsCounter >= epochtest:

      predictions = model.predict(xData_test)

      counterError = 0
      numberError = 0
      predictionError = 0.0
      predictionErrorMin = 1.0
      predictionErrorBadBit = 0.0
      predictionErrorBadBitMin = 1.0
      predictionErrorBadBitMax = 0.0

      predictionErrorPerBit = np.zeros(len(predictions[0]))
      predictionErrorPerBitMin = np.ones(len(predictions[0]))
      predictionErrorPerBitMax = np.zeros(len(predictions[0]))

      for x in range(len(predictions)):
          numberErrorInner = 0
          for y in range(len(predictions[x])):

              error = np.abs(yData_test[x][y]-predictions[x][y])
              predictionError += error
              predictionErrorPerBit[y] += error

              if (predictionErrorMin > error):
                  predictionErrorMin = error

              if (predictionErrorPerBitMax[y] < error):
                  predictionErrorPerBitMax[y] = error

              if (predictionErrorPerBitMin[y] > error):
                  predictionErrorPerBitMin[y] = error

              if (error >= 0.2):
                  counterError += 1
                  numberErrorInner += 1
                  predictionErrorBadBit += error

                  if (predictionErrorBadBitMin > error):
                      predictionErrorBadBitMin = error

                  if (predictionErrorBadBitMax < error):
                      predictionErrorBadBitMax = error

          if (numberErrorInner > 0):
              numberError += 1

      if (numberError != 0):
          print("")

      predictionError /= (len(predictions) * len(predictions[0]))

      for y in range(len(predictions[0])):
          predictionErrorPerBit[y] /= len(predictions)

      if (predictionErrorBadBit > 0):
          predictionErrorBadBit /= counterError
      else:
          predictionErrorBadBit = 0

      np.set_printoptions(precision=4)

      print("counterError : ", counterError, "/", (len(predictions) * len(predictions[0])), " - rate : ", (counterError/(len(predictions) * len(predictions[0]))))
      print("numberError : ", numberError, "/", len(predictions), " - rate : ", numberError / len(predictions))
      print("predictionError : ", predictionError, " - min : ", predictionErrorMin)
      print("predictionErrorBadBit : ", predictionErrorBadBit, " - min : ", predictionErrorBadBitMin, " max : ", predictionErrorBadBitMax)
      print("")
      print("predictionErrorPerBit : ")
      print(predictionErrorPerBit)
      print("")
      print("predictionErrorPerBitMin : ")
      print(predictionErrorPerBitMin)
      print("")
      print("predictionErrorPerBitMax : ")
      print(predictionErrorPerBitMax)
      print("")

      if (numberError / len(predictions) < reccord):
          model.save('./ctr-20p.h5')
          reccord = numberError / len(predictions)
          print("new reccord : ", reccord)

      if (epochsCounter >= maximumEpochs):
          model = Sequential()
          initial = True
          epochsCounter = 0
          print("reset neural network")

      if (numberError == 0):
          print("model : ", counterModel)
          break
