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
        citypart2 = citypart2.replace(",", "")
        city = citypart1 + " " + citypart2
        statepart1 = city_data[3]
        statepart2 = city_data[4]
        state = statepart1 + " " + statepart2
        
        average_hourly = city_data[6]

    elif city_data[1]== 'Charlotte,':
        ranking = city_data[0]
        ranking = ranking.replace(".", "")
        city = city_data[1]
        statepart1 = city_data[2]
        statepart2 = city_data[3]
        state = statepart1 + " " + statepart2
        average_hourly = city_data[5]

    elif len(city_data) == 6:
        ranking = city_data[0]
        ranking = ranking.replace(".", "")
        citypart1 = city_data[1]
        citypart2 = city_data[2]
        #city = city.append(city_data[2])
        citypart2 = citypart2.replace(",", "")
        city = citypart1 + " " + citypart2
        state = city_data[3]
        average_hourly = city_data[5]

    else:
        ranking = city_data[0]
        ranking = ranking.replace(".", "")
        city = city_data[1]
        city = city.replace(",", "")
        state = city_data[2]
        average_hourly = city_data[4]
        
    summary = (ranking, city, state, average_hourly)
    salaries_sum.append(summary)

#setting up database
db_name = 'Salary Analysis'
path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(path+'/'+db_name)
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS Salaries")
cur.execute("CREATE TABLE Salaries (ranking INTEGER PRIMARY KEY, state TEXT, city TEXT, average_hourly TEXT)")
for ranking in salaries_sum:
    cur.execute("INSERT INTO Salaries (ranking, state, city, average_hourly) VALUES (?,?,?,?)", ranking)
conn.commit()