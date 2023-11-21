import requests
from bs4 import BeautifulSoup

url = 'https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads'

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find the table containing the player data
table = soup.find('table', class_='sortable')

# Find all rows with country names
countries = table.find_all('tr', {'class': 'nat-fs-player'})

for country in countries:
    # Extract country name
    country_name = country.find('td').find('a').text.strip()
    print(f"Country: {country_name}")

    # Extract player data for the country
    players = country.find_next_siblings('tr')
    
    for player in players:
        columns = player.find_all(['th', 'td'])
        if len(columns) > 1:
            number = columns[0].text.strip()
            position_raw = columns[1].text.strip()
            position = ''.join([char for char in position_raw if not char.isdigit()]).strip()
            player_name = columns[2].find('a').text.strip()
            date_of_birth = columns[3].text.strip()
            age = int(date_of_birth[date_of_birth.rfind('(') + 5: -1])
            caps = columns[4].text.strip()
            goals = columns[5].text.strip()
            club = columns[6].text.strip()
            
            # Print the extracted data (you can process or store it as needed)
            print(f"Number: {number}, Position: {position}, Player: {player_name}, Age: {age}, Caps: {caps}, Goals: {goals}, Club: {club}")
