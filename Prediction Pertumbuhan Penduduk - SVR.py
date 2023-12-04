# -*- coding: utf-8 -*-
"""PREDIKSI PERTUMBUHAN PENDUDUK

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BXr0O-PAslUoGVC8qv3PQshwK7WVtG33
"""

import pandas as pd
import numpy as np
from sklearn.svm import SVR

df = pd.read_csv('/content/data_jat (1).csv')
df

df.info()

df["JUMLAH PENDUDUK"] = df["JUMLAH PENDUDUK"].astype("float")

df.info()

#Independent Dependent Variable
x = df.iloc[:,[0]].values
y = df.iloc[:,[1]].values

#Split Train Test Data

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.20, random_state=20)

# Training
from sklearn.linear_model import LinearRegression

regresi = LinearRegression()
regresi.fit(x_train, y_train)
y_predi = regresi.predict(x_test)

lin_svr = SVR(kernel='linear', C=1e3)
lin_svr.fit(x_train, y_train)
y_predic = lin_svr.predict(x_test)

print("Accuracy:",lin_svr.score(x_test, y_predic))

print("Accuracy:",regresi.score(x_test, y_predi))

from sklearn.metrics import mean_absolute_percentage_error, r2_score
print("MAPE :", mean_absolute_percentage_error(y_test,y_predic))
print("R2 : ", r2_score(y_test,y_predic))

#prediksi data baru
df_baru = pd.read_csv('/content/prediksi.csv')

predicted = lin_svr.predict(df_baru)
predicted

import matplotlib.pyplot as plt
plt.figure(figsize=(8,5))
plt.title('visualisasi data hasil prediksi dari data test')

plt.scatter(x_test,y_test, c='blue')

plt.plot(x_test,y_predic, c='black')

plt.scatter(df_baru,predicted, c='red')
plt.xlabel("Tahun")
plt.ylabel("Jumlah")
plt.grid()

"""SVM"""

#Import the libraries
from sklearn.svm import SVR
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('seaborn-darkgrid')

def predict_population(x_train, y_train, x):
    lin_svr = SVR(kernel='linear', C=1000.0)
    lin_svr.fit(x_train, y_train)#Create and train an SVR model using a polynomial kernel

    poly_svr = SVR(kernel='poly', C=1000.0, degree=2)
    poly_svr.fit(x_train, y_train)

    svr_rbf = SVR(kernel='rbf', C=1000.0, gamma=0.15)
    svr_rbf.fit(x_train, y_train)

    plt.scatter(x_train, y_train, color = 'black', label='Data')
    plt.plot(x_train, poly_svr.predict(x_train),color='red', label= 'poly_svr')
    plt.xlabel('year')
    plt.ylabel('population')
    plt.legend()
    plt.show()

    return poly_svr.predict(x)[0]

predicted = predict_population(x_train, y_train, [[2024]])
print(predicted)

#Create and train an SVR model using a linear kernel
lin_svr = SVR(kernel='linear', C=1000.0)
lin_svr.fit(x_train, y_train)#Create and train an SVR model using a polynomial kernel
poly_svr = SVR(kernel='poly', C=1000.0, degree=2)
poly_svr.fit(x_train, y_train)#Create and train an SVR model using a RBF kernel
rbf_svr = SVR(kernel='rbf', C=1000.0, gamma=0.15)
rbf_svr.fit(x_train, y_train)

year = [[2022]]
print('The RBF SVR predicted:', rbf_svr.predict(year))
print('The Linear SVR predicted:', lin_svr.predict(year))
print('The Polynomial SVR predicted:', poly_svr.predict(year))

plt.figure(figsize=(16,8))
plt.scatter(x_train, y_train, color = 'black', label='Original Data')
plt.plot(x_train, lin_svr.predict(x_train), color = 'purple', label='Linear Model')
plt.xlabel('year')
plt.ylabel('jumlah penduduk')
plt.title('Support Vector Regression')
plt.legend()
plt.show()

predicted_case = predict_cases()