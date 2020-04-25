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

#
# Your name: Ruthie Dingeldein and Clare McAuliffe
#


#gathering data for populations per city
article_url = 'https://www.governing.com/gov-data/population-density-land-area-cities-map.html'
p = requests.get(article_url)
page = p.text
soup = BeautifulSoup(page, 'html.parser')
city_summaries = []
for city_data in soup.find_all('tr'):
    city_data = city_data.text
    city_data = city_data.strip()
    city_data = city_data.split('\n')
    city = city_data[0]
    population_density = city_data[1]
    population = city_data[2]
    land_area = city_data[3]
    summary = (city, population_density, population, land_area)
    city_summaries.append(summary)

#setting up database
db_name = 'Population Analysis'
path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(path+'/'+db_name)
cur = conn.cursor()

#setting up Populations Table
cur.execute("DROP TABLE IF EXISTS Populations")
cur.execute("CREATE TABLE Populations (city TEXT PRIMARY KEY, population_density INTEGER, population INTEGER, land_area INTEGER)")
minimum = 0
maximum = 20
for i in range(20):
    for city in city_summaries[minimum:maximum]:
        cur.execute("INSERT INTO Populations (city, population_density, population, land_area) VALUES (?,?,?,?)", city)
    minimum += 20
    maximum += 20

conn.commit()

#setting up Type Table
cur.execute("DROP TABLE IF EXISTS Type")
cur.execute("CREATE TABLE Type (city TEXT PRIMARY KEY, type TEXT)")
minimum = 1
maximum = 20
for i in range(20):
    for city in city_summaries[minimum:maximum]:
        if int(city[1].replace(',', '')) < 5000:
            cur.execute("INSERT INTO Type (city, type) VALUES (?, ?)", (city[0], 'Small'))
        elif int(city[1].replace(',', '')) < 10000:
            cur.execute("INSERT INTO Type (city, type) VALUES (?, ?)", (city[0], 'Medium'))
        else:
            cur.execute("INSERT INTO Type (city, type) VALUES (?, ?)", (city[0], 'Large'))
    minimum += 20
    maximum += 20
conn.commit()

#gathering data for populations per city
article_url = 'https://www.businessinsider.com/highest-earning-cities-uber-lyft-2019-12'
p = requests.get(article_url)
page = p.text
soup = BeautifulSoup(page, 'html.parser')
salaries_sum = []
headers = soup.find_all('h2', class_ = 'slide-title-text')

for city_data in headers:
    city_data = city_data.text
    city_data = city_data.strip()
    city_data = city_data.split()

    if city_data[2]== 'York,':
        ranking = city_data[0]
        ranking = ranking.replace(".", "")
        citypart1 = city_data[1]
        citypart2 = city_data[2]
        #citypart2 = citypart2.replace(",", "")
        city = citypart1 + " " + citypart2
        statepart1 = city_data[3]
        statepart2 = city_data[4]
        citystate = city + " " +statepart1 + " " + statepart2
        
        average_hourly = city_data[6]

    elif city_data[1]== 'Charlotte,':
        ranking = city_data[0]
        ranking = ranking.replace(".", "")
        city = city_data[1]
        statepart1 = city_data[2]
        statepart2 = city_data[3]
        citystate = city + " " + statepart1 + " " + statepart2 
        average_hourly = city_data[5]

    elif len(city_data) == 6:
        ranking = city_data[0]
        ranking = ranking.replace(".", "")
        citypart1 = city_data[1]
        citypart2 = city_data[2]
        #citypart2 = citypart2.replace(",", "")
        city = citypart1 + " " + citypart2
        citystate = city + " " + city_data[3]
        average_hourly = city_data[5]

    else:
        ranking = city_data[0]
        ranking = ranking.replace(".", "")
        city = city_data[1]
        #city = city.replace(",", "")
        citystate = city + " " +city_data[2]
        average_hourly = city_data[4]
        
    summary = (ranking, citystate, average_hourly)
    salaries_sum.append(summary)


cur.execute("DROP TABLE IF EXISTS Salaries")
cur.execute("CREATE TABLE Salaries (ranking INTEGER PRIMARY KEY, citystate TEXT, average_hourly TEXT)")
minimum = 0
maximum = 16
for i in range(2):
    for ranking in salaries_sum[minimum:maximum]:
        cur.execute("INSERT INTO Salaries (ranking, citystate, average_hourly) VALUES (?,?,?)", ranking)
    minimum = 16
    maximum = 33
conn.commit()

#joining the databases 
cur.execute('SELECT city, population_density, Salaries.ranking, Salaries.average_hourly FROM Populations INNER JOIN Salaries ON Populations.city = Salaries.citystate')
rest = cur.fetchall()
conn.commit()

#first figure 
plt.ylabel('Hourly Salary')
plt.xlabel('Population Density')
hourlysalaries = []
popdensities = []
for city in reversed(rest):
    density = city[1].replace(",","")
    popdensities.append(int(density))
    sal = city[3].replace("$","")
    hourlysalaries.append((sal))
plt.scatter(popdensities, hourlysalaries, color='r')

#plt.show()

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




