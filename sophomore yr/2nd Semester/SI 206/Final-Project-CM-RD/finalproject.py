from bs4 import BeautifulSoup
import requests
import re
import csv
import json
import unittest
import os

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
print(city_summaries)

