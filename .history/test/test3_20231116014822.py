import requests
from bs4 import BeautifulSoup
import pandas as pd
import json


# Get the HTML content of the Wikipedia page
url = "https://en.wikipedia.org/wiki/List_of_European_stadiums_by_capacity"
response = requests.get(url)
html = response.text

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Find the table containing the stadium data
span = soup.find_all("span", {"class":'mw-headline'})[0]
span_rows = span.find_all('id')

print(span_rows)