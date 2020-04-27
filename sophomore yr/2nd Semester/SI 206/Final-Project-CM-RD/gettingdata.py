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

cur.execute("CREATE TABLE IF NOT EXISTS Populations (city TEXT PRIMARY KEY, population_density INTEGER, population INTEGER, land_area INTEGER)")
for i in range(30):
    cur.execute("SELECT * FROM Populations")
    index = len(cur.fetchall())
    if index <= len(city_summaries):
        for city in city_summaries[index:index+20]:
            cur.execute("INSERT OR IGNORE INTO Populations (city, population_density, population, land_area) VALUES (?,?,?,?)", city)
    i += 1
    conn.commit()



#setting up Type Table

cur.execute("CREATE TABLE IF NOT EXISTS Type (city TEXT PRIMARY KEY, type TEXT)")
for i in range(30):
    cur.execute("SELECT * FROM Type")
    index = len(cur.fetchall())
    if index <= len(city_summaries):
        for city in city_summaries[index:index+20]:
            if int(city[1].replace(',', '')) < 5000:
                cur.execute("INSERT OR IGNORE INTO Type (city, type) VALUES (?, ?)", (city[0], 'Small'))
            elif int(city[1].replace(',', '')) < 10000:
                cur.execute("INSERT OR IGNORE INTO Type (city, type) VALUES (?, ?)", (city[0], 'Medium'))
            else:
                cur.execute("INSERT OR IGNORE INTO Type (city, type) VALUES (?, ?)", (city[0], 'Large'))
    i += 1
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


cur.execute("CREATE TABLE IF NOT EXISTS Salaries (ranking INTEGER PRIMARY KEY, citystate TEXT, average_hourly TEXT)")
for i in range(2):
    cur.execute("SELECT * FROM Salaries")
    index = len(cur.fetchall())
    if index <= len(salaries_sum):
        for salary in salaries_sum[index:index+16]:
            cur.execute("INSERT OR IGNORE INTO Salaries (ranking, citystate, average_hourly) VALUES (?,?,?)", ranking)
    i += 1
    conn.commit()