import requests
from bs4 import BeautifulSoup

url = 'https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads'
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    for h3 in soup.find_all('h3'):
        country = h3.find('span', class_='mw-headline').text.strip()
    
    print(country)
    
    
