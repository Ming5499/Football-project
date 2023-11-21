import requests
from bs4 import BeautifulSoup
import pandas as pd
import json


# Get the HTML content of the Wikipedia page
NO_IMAGE = 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/No-image-available.png/480px-No-image-available.png'
url = "https://en.wikipedia.org/wiki/List_of_European_stadiums_by_capacity"
response = requests.get(url)
html = response.text

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Find the table containing the stadium data

for i in range(0,7):
    table = soup.find_all("table", {"class":'wikitable sortable'})[i]
    table_rows = table.find_all('tr')
    print(table_rows)