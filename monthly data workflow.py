""" Download and visualize montly global earth surface temperature data.
    Data are GLOBAL Land-Ocean Temperature Index in degrees Celsius with base period: 1951-1980"""
#Load Packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Load data
url = 'https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.txt'
data = pd.read_csv(url, skiprows = 7, delim_whitespace=True, index_col = 0, na_values='****')

#Prepare timeseries
d= data.drop(['Year.1', 'J-D','D-N','DJF','MAM','JJA','SON'], axis=1).drop(['Year', 'Divide', 'Multiply', 'Example', 'change'], axis=0).reset_index()
dlong = pd.melt(d, id_vars = 'Year', value_vars=['Jan','Feb', 'Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'], var_name='month')
dlong.index = pd.to_datetime(dlong['Year'].astype(str) + dlong['month'], format='%Y%b')
ts = pd.Series(dlong['value']).astype(float).sort_index()/100
ts
#compute 12 months moving average
movingaverage = ts.rolling(window = 12).mean()

#compute global mean
average =  ts.mean()
#Plot timeseries
start = '1879-01-01'
finish = '2027-01-01'
fig, ax = plt.subplots(figsize = (20,10))
plt.xlim(start, finish)
ts.plot(color='lightblue', marker='', linestyle='dashed', linewidth=1)
movingaverage.plot(color='b', marker='', linestyle='solid', linewidth=2)
plt.hlines(average, xmin = start, xmax = finish, color='darkblue', linestyle='solid', linewidth=1)
ax.set_title('Global Earth Surface Temperature')
ax.set_ylabel('Difference in degrees Celsius compared to 1951-1980 mean')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.legend(["Monthly", "12-Month average", "1879-2020 average"])
plt.show()
