import requests
from bs4 import BeautifulSoup

url = 'https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads'

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

country_names = []

count = 0  # Initialize a counter

for h3 in soup.find_all('h3'):
    if count < 32:  # Limit the loop to the first 32 iterations
        country_name = h3.find('span', class_='mw-headline').text
        country_names.append(country_name)
        count += 1

print(country_names)

import requests
from bs4 import BeautifulSoup

url = 'https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads'

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

country_names = []

for h3 in soup.find_all('h3', class_='mw-headline'):
    country_name = h3.find('span').text.strip()
    country_names.append(country_name)

print(country_names)

