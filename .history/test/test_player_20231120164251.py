import requests
from bs4 import BeautifulSoup

# Send a GET request to the URL
url = 'https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads'
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all tables containing player information
    tables = soup.find_all('table', class_='playerlist')

    # Extract player data from each table
    players = []
    for table in tables:
        for row in table.find_all('tr'):
            player_data = {}
            for cell in row.find_all('td'):
                key = cell.find('span', class_='mw-headline').text.strip()
                value = cell.find('span', {'class': ['player-squad', '']}).text.strip()
                player_data[key] = value

            # Add the player data to the list
            players.append(player_data)

    # Print the extracted player data
    for player in players:
        print(player)
else:
    print('Error fetching data from URL.')
