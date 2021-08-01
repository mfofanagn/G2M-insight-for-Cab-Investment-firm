import pandas as pd
import os
import xlrd
import math
#import pandas_profiling
import sweetviz
#from supervised.automl import AutoML
#from supervised.preprocessing.eda import EDA
import numpy as np

import datetime
from datetime import datetime, timedelta


os.chdir("D:/FOAD/DSTI/Data Glacer/DataSets/")

# I. Data set loading

cab_data = pd.read_csv("cab_data.csv")
city = pd.read_csv("city.csv", decimal=".")
#print(city.head(22))

#Formatting city data
city["Population"] = city["Population"].str.strip()
city["Population"] = [float(str(i).replace(",", "")) for i in city["Population"]]
city["Population"] = city["Population"].astype(float)
#
city["Users"] = city["Users"].str.strip()
city["Users"] = [float(str(i).replace(",", "")) for i in city["Users"]]
city["Users"] = city["Users"].astype(float)

print(city.info())

customer = pd.read_csv("Customer_ID.csv")
transaction = pd.read_csv("Transaction_ID.csv")

US_holiday = pd.read_csv("US Holiday Dates (2004-2021).csv")
holidays = pd.to_datetime(US_holiday['Date']).dt.date
#print(city.head())

temperature_US = pd.read_csv("US_City_temperature.csv")
#temperature_US = pd.read_csv("temp0.csv")
#emperature_US = temperature[(temperature.Country =='US') & (temperature.Year >= 2016) & (temperature.Year <= 2018)]
#print(temperature_US.head())
#temperature_US.to_csv("D:/DSTI/Data Glacer/DataSets/temp2.csv")

# II. Data merging
output1 = pd.merge(transaction, cab_data,
                   on='Transaction ID',
                   how='inner')

#print(output1.head())
#print(output1.shape)
#print(transaction.shape)

output2 = pd.merge(output1, customer,
                   on='Customer ID',
                   how='left')

#print(output2.shape)

output3 = pd.merge(output2, city,
                   on='City',
                   how='left')


#if (output3['Date of Travel'].isna() == False):
output3['Date of Travel'] = output3['Date of Travel'].apply(lambda s: xlrd.xldate.xldate_as_datetime(s, 0).date() if math.isnan(s) == False else s )
output3["Date of Travel"] = pd.to_datetime(output3["Date of Travel"])

output3["Year"] = pd.DatetimeIndex(output3['Date of Travel']).year
output3["Month"] = pd.DatetimeIndex(output3['Date of Travel']).month
output3["Day"] = pd.DatetimeIndex(output3['Date of Travel']).day

output4 = pd.merge(output3, temperature_US, how='left',
                   left_on=['City','Year', 'Month', 'Day'], right_on = ['City','Year', 'Month', 'Day'],)
#
# Adding of field Margin
output4["Margin"] =  output4["Price Charged"] - output4["Cost of Trip"]


#Adding of field Holiday
for index, row in output4.iterrows():
     if row["Date of Travel"] in holidays.values:
         row["Holiday"] = 1
         #output3[index] = row
         output4.at[index, 'Holiday'] = 1
     else:
        row["Holiday"] = 0
        #output3[index] = row
        output4.at[index, 'Holiday'] = 0

# Managing duplicate data
output5 = output4.drop_duplicates(subset=['Transaction ID'])
print(output5['Transaction ID'].duplicated().sum())
output5.to_csv("D:/FOAD/DSTI/Data Glacer/DataSets/G2M_Global_Dataset.csv")


# Checking null value
print(output5.isnull().values.sum())
print(output5.isnull().values.any())
print(output5.isna().any(axis=None))

print(output5.info())
print(output5.head())

#Automated explotaory data analysis
report = sweetviz.analyze(output5,target_feat='Margin',pairwise_analysis='on')
report.show_html(open_browser=True, filepath="D:/FOAD/DSTI/Data Glacer/DataSets/EDA_G2M.html", layout='widescreen')

#EDA.extensive_eda()

# Model building (Not yet finished)
from  sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.model_selection  import train_test_split
#from sklearn.

#mod = LinearRegression()
#X  = output3[["Customer ID", "Date of Travel","KM Travelled", "Price Charged","Cost of Trip", "Age", "Income (USD/Month)","Population","Users","Payment_Mode","Company","City", "Gender"]]
#X = pd.get_dummies(X, columns=["Payment_Mode", "Company", "City", "Gender"] )
#print(output3.info())
#X  = output3[["Customer ID","KM Travelled", "Price Charged","Cost of Trip", "Age"]]
#y = output5[["Margin"]]

# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
#
# mod.fit(X_train,y_train)
# pred = mod.predict(X_test)
#
# print(r2_score(y_test,pred))
# print(mean_squared_error(y_test, pred))