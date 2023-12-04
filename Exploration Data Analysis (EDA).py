# -*- coding: utf-8 -*-
"""Insight Supermarket Kelompok.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1trCtAmy-E19HER1CAzgShH0fQbxLB6rr
"""

# Basic Library
import pandas as pd
import numpy as np

# Library untuk visualisasi
import matplotlib.pyplot as plt
import seaborn as sns

# Library untuk MBA
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

# Import data dari Kaggle

!wget -O supermarket.csv https://raw.githubusercontent.com/dzeaulfath/Python/main/DataSet/supermarket_sales%20-%20Sheet1.csv

"""**General Insight**"""

#Menampilkan Data

df = pd.read_csv('supermarket.csv')
df.head()

#For Search duplicate Row

df.duplicated().sum()

#For Search Missing value from data

df.isna().sum()

"""**Analysis Next Step**"""

#Menghitung gender dari data

df['Gender'].value_counts()

# Membuat dummies dari gender

gender_dummies=pd.get_dummies(df['Gender'])
gender_dummies.head()

#Menampilkan Table berdasarkan Gender

df=pd.concat([df,gender_dummies],axis=1)
df.head(2)

#Menampilkan Grafik dari Gender Perempuan

plt.figure(figsize=(14,6))
sns.barplot(x='Product line',y='Female',data=df)

# Menampilkan Grafik dari gender Laki- Laki

plt.figure(figsize=(14,6))
sns.barplot(x='Product line',y='Male',data=df)

#Mencari Gross Income tertinggi dari Penjualan

plt.figure(figsize=(13,6))
sns.barplot(x="Product line",y="gross income",data=df)

# Mencari Rating dari Jenis Produk

xdata=[0,1,2,3,4,5,6,7,8,9,10]
plt.figure(figsize=(10,6))
sns.barplot(y=df['Product line'],x=df['Rating'])
plt.xticks(xdata)
plt.show()

#Menampilkan Quantity

dv=pd.DataFrame(df['Quantity'].value_counts())
dv

#Menampilkan Grafik dari Kuantitas

plt.figure(figsize=(10,6))
sns.barplot(x=dv.index,y=dv['Quantity'],palette='inferno')

"""**Insight Dari data diatas**

* Total Customers = 1000
* Total Females = 501
* Total Males = 499
* Min Rating = 4
* Max Rating = 10
* Average Rating = 6.97
* Best Average Rating in Food & Beverages
* Max Average Gross Income in Home & Lifestyle
* Min Average Gross Income in Fashion Accessories
* Maximum customers buys 10 quantities
* Max Average total bill in Home and lifestyle
* Min Average total bill in Fashion Accessories
* Maximum People pays through e-wallet
* Maximum people comes from Yangon City
* Max Average Sales of Fashion Accessories is from Females
* Max Average Sales of Health & Beauty is from Males

---


---



---



---

**Payment Section**
"""

#Show index/ jenis jenis dari Payment

df['Payment'].value_counts().keys()

#Cek seberapa banyak pelanggan menggunakan masing-masing metode Payment

df['Payment'].value_counts()

#Menampilkan Pie Chart dari masing masing Payment

plt.pie(df['Payment'].value_counts(),labels=df['Payment'].value_counts().keys(),autopct='%1.0f%%',radius=1.5)
plt.legend()
plt.show()

#Menampilkan rata-rata Kuantitas Pembelian dari masing-masing payment

df.groupby('Payment')['Quantity'].mean()

#Menampilkan mean dari masing masing metode payment

df.groupby('Payment')['Total'].mean()

"""**Insight Dari Payment diatas**

* Tidak ada perbedaan antara kuantitas pada masing masing jumlah pembayaran
* Tidak ada perbedaan yang mencolok terhadap total uang yang digunakan dalam setiap metode pembayaran

---



---



---

**Customer Type**
"""

#Menampilkan Grafik berdasarkan Customer Type dan Gender

fig1, ax1 = plt.subplots(figsize=(10,5))
sns.countplot(x = 'Customer type',hue='Gender',data=df)

#Menampilkan Gross income dari Tipe Customer

df.groupby('Customer type')['gross income'].sum()

# Menampilkan Pembayar Pajak terbanyak pada tipe Customer

df.groupby('Customer type')['Tax 5%'].sum()

"""**Insight dari Costumer Type**

* Perempuan lebih banyak sebagai customer membership daripada laki laki
* Pemasukan dari membership customer lebih banyak dari customer biasa, maka dari itu supermarket harus memperbanyak promo untuk mendapatkan membership baru
* Dan juga sudah sangat jelas bahwa customer membership lebih banyak membayar pajak dari customer biasa

---


---



---

**Branch and City Type**
"""

#Membandingkan Jumlah customer berdasarkan gender yang datang di tiap branch

fig1, ax1 = plt.subplots(figsize=(10,5))
sns.countplot(x='Branch',hue='Gender',data=df)

#Membandingkan Jumlah customer berdasarkan gender yang datang di tiap kota

fig1, ax1 = plt.subplots(figsize=(10,5))
sns.countplot(df['City'],hue=df['Gender'])

#Menampilkan Kota dengan pendapatan tertinggi

explode = (0.1, 0, 0)
fig1, ax1 = plt.subplots(figsize=(10,5))
ax1.pie(df.groupby('City')['gross income'].sum(),explode=explode, labels=df['City'].unique(), autopct='%1.1f%%',
        shadow=True, startangle=90)

# Equal digunakan agar pie chart berbentuk lingkaran
ax1.axis('equal')
plt.tight_layout()
plt.legend()
plt.show()

# Menampilkan Total Quantitas Pembelian di setiap branch

df.groupby('City')['Quantity'].sum()

#Menampilkan rata-rata Rating yang diberikan Pelanggan pada setiap branch

df.groupby('Branch')['Rating'].mean()



"""**Insight Dari Branch Type**

* Pada branch C pembeli perempuan lebih banyak, sehingga jika branch C difokuskan ke pembeli perempuan maka akan lebih meraup banyak keuntungan
* Kemudian Kota Napyitaw menghasilkan keuntungan sedikit lebih banyak dari yang lain
* Branch C mendapatkan penilaian paling buruk dari yang lain, sehingga branch C harus memperbaiki kinerjanya

---


---



---

**Rule Based Persona**
"""

# Mendefinisikan Kategori features dengan function

def grab_cat_names(dataframe, cat_th = 10, car_th = 20):

  # Masukan Semua Kolom Kategori
    cat_cols = [col for col in dataframe.columns if dataframe[col].dtypes == 'O']

 #Masukan jenis data non-categoric dengan unique value dibawah 10

    num_but_cat =  [col for col in dataframe.columns if dataframe[col].nunique() < cat_th and
                    dataframe[col].dtypes != 'O' ]

 # Masukan jenis data kategorik dengan unique values lebih dari 20
    cat_but_car = [col for col in dataframe.columns if dataframe[col].nunique() > car_th and
                   dataframe[col].dtypes == 'O']

 # Masukan Semua jenis data dari kolom categorical dan non-categorical dengan unique values kurang dari 10
    final_cat_cols = cat_cols + num_but_cat

 # Tanpa variable cat_but_car
    final_cat_cols =  [col for col in final_cat_cols if col not in cat_but_car]
    return  cat_cols, num_but_cat, cat_but_car, final_cat_cols

cat_cols, num_but_cat, cat_but_car, final_cat_cols = grab_cat_names(df)

# Menampilkan semua coloumn
cat_cols

# Menampilkan data non kategori
num_but_cat

# Menampilkan jenis data kategorik
cat_but_car

# Menampilkan semua data dari jenis kategori dan non-kategori
final_cat_cols

final_cat_cols=['Branch', 'City', 'Customer type', 'Gender', 'Product line', 'Payment']

# Memasukan data kategorik yang telah dipilih dimbah total revenue dan rating

agg_df = df.groupby(by=['Branch', 'City', 'Customer type',
                          'Gender', 'Product line', 'Payment', 'Rating']).\
                          agg({"Total" : "sum"}).sort_values("Total", ascending=False)
agg_df.head()



"""**ARIMA**"""

#Merubah Tipe data Date

df['Date'] = pd.to_datetime(df['Date'])
df.head(2)

yangon = df.loc[df['City'] == 'Yangon']
yangon.head()



#Membuang seluruh rows dan hanya mengambil data date dan Total

r_col = ['Invoice ID', 'Branch', 'City', 'Customer type', 'Gender',
       'Product line', 'Unit price', 'Quantity', 'Tax 5%',
       'Time', 'Payment', 'cogs', 'gross margin percentage', 'gross income',
       'Rating', 'Female', 'Male']


yangon.drop(r_col, axis =1 , inplace=True)
yangon.head()

#Merapikan bentuk table dan mensortir berdasarkan tanggal

yangon = yangon[["Date","Total"]].sort_values('Date')
yangon.head()

# Untuk memasukan hasil sorting kedalam table yangon

yangon.set_index('Date', inplace=True)
yangon

# Membuat grafik dari yangob

yangon.plot(figsize=(15,6),legend=True)
plt.ylabel("Sales",fontsize=18)
plt.xlabel("Date",fontsize=18)
plt.title("Date Vs Sales",fontsize=20)
plt.show()



"""**Test Stationary**"""

#Import Library untuk testing

from statsmodels.tsa.stattools import adfuller

test_result = adfuller(yangon['Total'])
test_result



"""**We're using Dickey Fuller Test here to test for stationarity. The Dickey Fuller Test gives us 5 values, namely - ADF Test Statitic, p-value, #Lags used & Number of Observations used. However, our main focus here is on the p-value.**
.

.













We are assuming our H0 as "Our data is not stationary" and H1 as "Our data is stationary".

.

.









From the above 5 values, we see that our p-value is 2.034195712964938e-30 which is 0.000000000000000000000000000002034195712964938 in real numbers. Therefore, we can see that our p-value is less than 0.05 and hence we cannot accept our null hypothesis and that the data is stationary.
"""



"""**Resampling Data**"""

#Resampling the data using Calender Day Frequency and taking their average
yangon = yangon['Total'].resample('D').mean()
yangon.head()
# D = Calendar Day frequency

# Import Libray

import statsmodels.api as sm
from pylab import rcParams as rc

rc['figure.figsize'] = 10, 14
decomposition = sm.tsa.seasonal_decompose(yangon,model='additive', freq=30)

#Finding trend,seasonal,observed and residual values
fig = decomposition.plot()
plt.show()
# y(t) = Level + Trend + Seasonality + Noise --> Additive



"""**Forecasting with Arima**"""

# Import Library
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import itertools

fig = sm.graphics.tsa.plot_acf(yangon, lags=40)

fig = sm.graphics.tsa.plot_pacf(yangon, lags=40)

p=d=q=range(0,2)
p,d,q

pdq = list(itertools.product(p,d,q))
pdq

seasonal_pdq = [(x[0],x[1],x[2], 12) for x in pdq]
seasonal_pdq

for param in pdq:
    for param_seasonal in seasonal_pdq:
        try:
            mod = sm.tsa.statespace.SARIMAX(yangon,order = param, seasonal_order = param_seasonal ,
                                            enforce_stationarity= False , enforce_invertibility= False )
            results = mod.fit()

            print('ARIMA{} x {} 12 -- AIC : {}'.format(param, param_seasonal, results.aic))

        except:
             continue

mod = sm.tsa.statespace.SARIMAX(yangon,
                               order=(1,0,1),
                               seasonal_order= (1,1,1,12),
                               enforce_stationarity = False,
                               enforce_invertibility=False)
results = mod.fit()
print(results.summary().tables[1])

results.plot_diagnostics(figsize=(16,8))
plt.show()

pred = results.get_prediction(start = pd.to_datetime('2019-01-01'), dynamic = False)
pred_ci = pred.conf_int()

ax = yangon['2019':].plot(label= 'observed')

pred.predicted_mean.plot(ax = ax, label = 'One step ahead Forecast',
                        alpha = 7, figsize= (14,7))

ax.fill_between(pred_ci.index,
               pred_ci.iloc[:,0],
               pred_ci.iloc[:,1],color = 'k', alpha= 0.2)

ax.set_xlabel('Date')
ax.set_ylabel('Total')
plt.legend()

plt.show()

yangon_forecasted = pred.predicted_mean
yangon_truth = yangon['2019-01-01':]
mse = ((yangon_forecasted - yangon_truth) ** 2).mean()

print('MSE of forecast :{}'.format(round(mse,2)))

#Menggunakan 10 steps untuk memprediksi 10 hari kedepan

pred_uc = results.get_forecast(steps = 10)
pred_ci = pred_uc.conf_int()

ax = yangon.plot(label='observed', figsize=(10,8))
pred_uc.predicted_mean.plot(ax=ax, label='Forecast')
ax.fill_between(pred_ci.index,
               pred_ci.iloc[:,0],
               pred_ci.iloc[:,1],color='k',alpha=0.6)
ax.set_xlabel('Date')
ax.set_ylabel('Total')

plt.legend()
plt.show()

# Menganlisa Dengan 60 Steps atau 2 bulan

pred_uc = results.get_forecast(steps = 60)
pred_ci = pred_uc.conf_int()

ax = yangon.plot(label='observed', figsize=(10,8))
pred_uc.predicted_mean.plot(ax=ax, label='Forecast')
ax.fill_between(pred_ci.index,
               pred_ci.iloc[:,0],
               pred_ci.iloc[:,1],color='k',alpha=0.6)
ax.set_xlabel('Date')
ax.set_ylabel('Total')

plt.legend()
plt.show()