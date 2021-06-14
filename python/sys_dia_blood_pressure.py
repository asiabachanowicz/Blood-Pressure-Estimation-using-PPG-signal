import numpy as np
import pandas as pd
from keras.layers import *
from keras.models import Sequential, load_model
from keras.utils.vis_utils import plot_model
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
from keras.models import Model
from ann_visualizer.visualize import ann_viz;
from keras.models import model_from_json

# data pre-processing
os.chdir("C:/Users/Asia/Desktop/Praca/python")

# import data
data = pandas.read_csv("data.csv", sep=",")
data = data[["cp", "st", "dt", "sw10", "dw10", "sw10+dw10", "dw10/sw10", "sw25", "dw25",
             "sw25+dw25", "dw25/sw25", "sw33", "dw33", "sw33+dw33", "dw33/sw33", "sw50",
             "dw50", "sw50+dw50", "dw50/sw50", "sw66", "dw66", "sw66+dw66", "dw66/sw66",
             "sw75", "dw75", "sw75+dw75", "dw75/sw75", "sys", "dia"]]

# x (parameters) and y (blood pressure) data
predict1 = "sys"
predict2 = "dia"

X = numpy.array(data.drop([predict1, predict2], 1))
y = numpy.array(data[[predict1, predict2]])

# Splitting the total data into subsets: 70% - training, 30% - testing
X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, test_size=0.3)
X_test, X_val, y_test, y_val = sklearn.model_selection.train_test_split(X_test, y_test, test_size=0.5)

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
# model.add(Dense(50, input_shape=(27, ), activation='relu'))
# # model.add(BatchNormalization())
# model.add(Dense(30, activation='relu'))
# # model.add(BatchNormalization())
# model.add(Dense(20, activation='relu'))
# # model.add(BatchNormalization())
# model.add(Dense(10, activation='linear'))
# # model.add(BatchNormalization())
# model.add(Dense(2, activation='linear'))
#
# model.compile(optimizer='adam', loss='mse', metrics=['mse'])
# model.summary()
#
# # Early stopping to prevent overfitting
# model.compile(optimizer='adam', loss='mse', metrics=['mse'])
# monitor = EarlyStopping(monitor='val_loss', min_delta=1e-3, patience=50, verbose=1, mode='auto',
#                         restore_best_weights=True)
# history = model.fit(X_train_standardized, y_train, epochs=500, batch_size=200, verbose=1, callbacks=[monitor],
#                     validation_data=(X_val_standardized, y_val))
#
# # Summarize history for loss
# plt.plot(history.history['loss'])
# plt.title('model loss')
# plt.ylabel('loss')
# plt.xlabel('epoch')
# plt.show()
# -------------------------------------------------------------------------------------------------------------------#
# Load model
model = load_model('model_81.h5')
model.load_weights('weights_81.h5')
model.summary()

# Test the model and measure RMSE error
y_pred = model.predict(X_test_standardized)
score1 = numpy.sqrt(sklearn.metrics.mean_squared_error(y_pred[:,0], y_test[:,0]))
print(f"Final score (RMSE) for systolic blood pressure: {score1}")
score2 = numpy.sqrt(sklearn.metrics.mean_squared_error(y_pred[:,1], y_test[:,1]))
print(f"Final score (RMSE) for diastolic blood pressure: {score2}")

# Plot the output data
plt.plot(y_test[:,0], 'o', color='red', label='Real systolic BP')
plt.plot(y_pred[:,0], 'o', color='blue', label='Predicted systolic BP')
plt.plot(y_test[:,1], 'o', color='green', label='Real diastolic BP')
plt.plot(y_pred[:,1], 'o', color='yellow', label='Predicted diastolic BP')
plt.title('Prediction')
plt.legend()
plt.show()

# histogram MSE
y_pred1 = y_pred[:, 0].ravel()
error1 = y_pred1 - y_test[:, 0]
y_pred2 = y_pred[:, 1].ravel()
error2 = y_pred2 - y_test[:, 1]

plt.hist(error1, alpha=0.5, label='ciśnienie skurczowe')
plt.hist(error2, alpha=0.5, label='ciśnienie rozkurczowe')
plt.xlabel("Błąd estymacji ciśnienia krwi[mmHg]")
_ = plt.ylabel("Liczba próbek")
plt.show()