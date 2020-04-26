from bs4 import BeautifulSoup
import requests
import re
import csv
import json
import unittest
import os
import sqlite3
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
from geopy.geocoders import Nominatim
import math

#
# Your name: Ruthie Dingeldein and Clare McAuliffe
#

#setting up database
db_name = 'Population Analysis'
path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(path+'/'+db_name)
cur = conn.cursor()

#joining the databases 
cur.execute('SELECT city, population_density, Salaries.ranking, Salaries.average_hourly, population FROM Populations INNER JOIN Salaries ON Populations.city = Salaries.citystate')
rest = cur.fetchall()
conn.commit()

#first figure 
plt.ylabel('Hourly Salary')
plt.xlabel('Population Density')
plt.title("Relationship between uber/lyft salaires and population density")
hourlysalaries = []
popdensities = []
for city in reversed(rest):
    density = city[1].replace(",","")
    popdensities.append(int(density))
    sal = city[3].replace("$","")
    hourlysalaries.append((sal))
plt.scatter(popdensities, hourlysalaries, color='r')

plt.show()

#relation between pop and salary  
plt.ylabel('Hourly Salary')
plt.xlabel('Population')
plt.title("Relationship between uber/lyft salaires and population")
hourlysalaries = []
popdensities = []
for city in reversed(rest):
    density = city[4].replace(",","")
    popdensities.append(int(density))
    sal = city[3].replace("$","")
    hourlysalaries.append((sal))
plt.scatter(popdensities, hourlysalaries, color='g')

plt.show()


#average salary by city type 
small_total = 0
small_count = 0
medium_total = 0
medium_count = 0
large_total = 0
large_count = 0
for city in rest:
    if int(city[1].replace(',', '')) < 5000:
        small_total += float(city[3][1:])
        small_count += 1
    elif int(city[1].replace(',', '')) < 10000:
        medium_total += float(city[3][1:])
        medium_count += 1
    else:
        large_total += float(city[3][1:])
        large_count += 1
small_average = small_total/small_count
medium_average = medium_total/medium_count
large_average = large_total/large_count

#second figure
plt.ylabel('Average Hourly Salary')
plt.xlabel('City Size')
plt.title("Relationship between uber/lyft salaries and city size")

size = ('Small', 'Medium', 'Large')
y_pos = np.arange(len(size))
hourly = [small_average, medium_average, large_average]

plt.bar(y_pos, hourly, align='center', alpha=0.5, color = 'b', edgecolor='blue')
plt.xticks(y_pos, size)
plt.show()

#third figure
topfive = []
cur.execute('SELECT citystate FROM Salaries')
topthree = cur.fetchall()
topthree = topthree[0:3]


#map plotting that works
fig = plt.figure(figsize=(7, 7))
m = Basemap(projection='lcc', resolution=None,
            width=8E6, height=8E6, 
            lat_0=45, lon_0=-100,)
m.etopo(scale=0.5, alpha=0.5)

# Map (long, lat) to (x, y) for plotting
x, y = m(-122.3, 39)
plt.plot(x, y, 'ok', markersize=3)
plt.text(x, y, topthree[0][0], fontsize=8)
#second
x, y = m(-122.3, 47)
plt.plot(x, y, 'ok', markersize=3)
plt.text(x, y, topthree[1][0], fontsize=8)
#third
x, y = m(-121, 36)
plt.plot(x, y, 'ok', markersize=3)
plt.text(x, y, topthree[2][0], fontsize=8)
plt.show()



