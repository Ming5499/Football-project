import requests
from bs4 import BeautifulSoup

url = 'https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads'

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

country_names = []

for h3 in soup.find_all('h3'):
    country_name = h3.find('span', class_='mw-headline').text
    country_names.append(country_name)

print(country_names)
