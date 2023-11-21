import requests
from bs4 import BeautifulSoup

url = 'https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads'

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

country_names = []

for h3 in soup.find_all('h3', class_='mw-headline'):
    country_name = h3.find('span').text.strip()  # Retrieve the text within the span element and strip whitespace
    if 'Age' not in country_name and 'Squads' not in country_name:  # Ignore sections related to squad statistics
        country_names.append(country_name)

# Print the list of country names without additional text
print(country_names)
