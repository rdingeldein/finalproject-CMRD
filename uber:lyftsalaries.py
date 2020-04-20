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

    ranking = city_data[0]
    ranking = ranking.replace(".", "")
    city = city_data[1]
    city = city.replace(",", "")
    state = city_data[2]
    average_hourly = city_data[4]
    
    summary = (ranking, city, state, average_hourly)
    salaries_sum.append(summary)

#setting up database
db_name = 'Uber/lyft Hourly Salary Analysis'
path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(path+'/'+db_name)
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS Salaries")
cur.execute("CREATE TABLE Salaries (ranking INTEGER, state TEXT PRIMARY KEY, city TEXT PRIMARY KEY, average_hourly TEXT PRIMARY KEY)")
for ranking in salaries_sum:
    cur.execute("INSERT INTO Salaries (ranking, state, city, average_hourly) VALUES (?,?,?,?)", ranking)
conn.commit()