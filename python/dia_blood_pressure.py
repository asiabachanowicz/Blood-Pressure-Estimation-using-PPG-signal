import numpy as np
import pandas as pd
from keras.layers import *
from keras.models import Sequential, load_model
from keras.optimizers import *
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import *
from sklearn.decomposition import PCA
import os
from keras.callbacks import EarlyStopping
from keras.callbacks import ModelCheckpoint
import tensorflow
import keras
import pathlib
import matplotlib.pyplot as plt
import sklearn
import pandas
import numpy
import sklearn
from sklearn import linear_model
from sklearn.utils import shuffle
from keras.layers import Dense
from keras.layers import Activation
from keras.models import Sequential
from sklearn.metrics import mean_squared_error
from math import sqrt
import seaborn
import pickle

# data pre-processing
os.chdir("C:/Users/Asia/Desktop/Praca/python")

# import data
data = pandas.read_csv("data.csv", sep=",")
data = data[["cp", "st", "dt", "sw10", "dw10", "sw10+dw10", "dw10/sw10", "sw25", "dw25",
             "sw25+dw25", "dw25/sw25", "sw33", "dw33", "sw33+dw33", "dw33/sw33", "sw50",
             "dw50", "sw50+dw50", "dw50/sw50", "sw66", "dw66", "sw66+dw66", "dw66/sw66",
             "sw75", "dw75", "sw75+dw75", "dw75/sw75", "dia"]]

# data description
described_data = data.describe()
print(described_data)
print(len(data))

# # histograms of input data (features)
# data.hist(figsize=(12, 10))
# plt.show()

# index and shuffle data
data.reset_index(inplace=True, drop=True)
data = data.reindex(numpy.random.permutation(data.index))

# x (parameters) and y (blood pressure) data
predict = "dia"
X = numpy.array(data.drop([predict], 1))
y = numpy.array(data[predict])

# Splitting the total data into subsets: 70% - training, 15% - testing, 15% - validation
X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, test_size=0.3, random_state=0)
X_test, X_val, y_test, y_val = sklearn.model_selection.train_test_split(X_test, y_test, test_size=0.5, random_state=0)

def feature_normalize(X):   # standardization function
    mean = numpy.mean(X, axis=0)
    std = numpy.std(X, axis=0)
    return (X - mean) / std


# Features scaling
X_standardized = feature_normalize(X)
X_train_standardized = feature_normalize(X_train)
X_test_standardized = feature_normalize(X_test)
X_val_standardized = feature_normalize(X_val)

#----------------------------------------------------------------------------------------------------------------------#
# # Build the ANN model
# model = Sequential()
# model.add(Dense(50, input_shape=(27, ), activation='sigmoid'))
# model.add(BatchNormalization())
# model.add(Dense(30, activation='sigmoid'))
# model.add(BatchNormalization())
# model.add(Dense(20, activation='sigmoid'))
# model.add(BatchNormalization())
# model.add(Dense(10, activation='linear'))
# model.add(BatchNormalization())
# model.add(Dense(1, activation='linear'))
# model.compile(optimizer='adam', loss='mse', metrics=['mse'])
# # model.summary()
#
# # Early stopping to prevent overfitting
# monitor = EarlyStopping(monitor='val_loss', min_delta=1e-3, patience=50, verbose=1, mode='auto',
#                         restore_best_weights=True)
# history = model.fit(X_train_standardized, y_train, epochs=500, batch_size=200, verbose=1, callbacks=[monitor],
#                     validation_data=(X_val_standardized, y_val))
#
# # Summarize history for loss
# plt.plot(history.history['loss'])
# plt.plot(history.history['val_loss'])
# plt.title('model loss')
# plt.ylabel('loss')
# plt.xlabel('epoch')
# plt.legend(['train', 'val'], loc='upper left')
# plt.show()
#----------------------------------------------------------------------------------------------------------------------#
# Load model
model = load_model('model_52.h5')
model.load_weights('weights_52.h5')
model.summary()

# Test the model and measure RMSE error
y_pred = model.predict(X_test_standardized)
score = numpy.sqrt(sklearn.metrics.mean_squared_error(y_pred, y_test))

loss, mse = model.evaluate(X_test_standardized, y_test, verbose=2)
print("Test model mse: {:5.2f}".format(mse))
print(f"Final score (RMSE): {score}")

# Plot the output data
plt.plot(y_test, 'o', color='red', label='Real data')
plt.plot(y_pred, 'o', color='blue', label='Predicted data')
plt.title('Prediction')
plt.legend()
plt.show()

y_pred = y_pred.ravel()

# histogram mmHg for test
error = y_pred - y_test
plt.hist(error, bins = 25)
plt.xlabel("Błąd estymacji ciśnienia krwi[mmHg]")
_ = plt.ylabel("Liczba próbek")
plt.show()