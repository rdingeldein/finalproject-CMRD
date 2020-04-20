from bs4 import BeautifulSoup
import requests
import re
import csv
import json
import unittest
import os
import sqlite3


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
for city in city_summaries:
    cur.execute("INSERT INTO Populations (city, population_density, population, land_area) VALUES (?,?,?,?)", city)
conn.commit()

#setting up Type Table
cur.execute("DROP TABLE IF EXISTS Type")
cur.execute("CREATE TABLE Type (city TEXT PRIMARY KEY, type TEXT)")
for city in city_summaries[1:]:
    if int(city[1].replace(',', '')) < 5000:
        cur.execute("INSERT INTO Type (city, type) VALUES (?, ?)", (city[0], 'Small'))
    elif int(city[1].replace(',', '')) < 10000:
        cur.execute("INSERT INTO Type (city, type) VALUES (?, ?)", (city[0], 'Medium'))
    else:
        cur.execute("INSERT INTO Type (city, type) VALUES (?, ?)", (city[0], 'Large'))
conn.commit()


