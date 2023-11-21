import requests
from bs4 import BeautifulSoup
import pandas as pd
import json


# Get the HTML content of the Wikipedia page

url = "https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads"
response = requests.get(url)
html = response.text

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')



table = soup.find_all("table", {"class":'sortable wikitable plainrowheaders jquery-tablesorter'})
# table_rows = table.find_all('tr')
print(table)

