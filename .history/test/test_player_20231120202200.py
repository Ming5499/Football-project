import requests
from bs4 import BeautifulSoup
import csv
url = 'https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads'

# List of groups from A to H
groups = ['Group_A']

player_count = 0  # Initialize player count
player_data = []  # List to store player data
for group in groups:
    # Extract country name from the table header row for the first player
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    tables = soup.find_all('table', class_='sortable')
    for table in tables:
        row = table.find_all('tr')[1]

        for row in table.find_all('tr')[2:]:
            player_count += 1
            columns = row.find_all(['th', 'td'])

            anchor_tag = columns[2].find('a')
            if anchor_tag is None:
                player_name = 'N/A'  # Handle missing player name
            else:
                player_name = anchor_tag.text.strip()

            date_of_birth = columns[3].text.strip()
            age = int(date_of_birth[date_of_birth.rfind('(') + 5: -1])
            club = columns[6].text.strip()

            print(f"Number: {player_count}, Player Name: {player_name}, Age: {age}, Club: {club}, Group: {group.split('_')[-1]}")

            
            