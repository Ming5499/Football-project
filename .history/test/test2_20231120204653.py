import requests
from bs4 import BeautifulSoup
import csv

url = 'https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads'

player_count = 0  # Initialize player count
player_data = []  # List to store player data

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
tables = soup.find_all('table', class_='sortable')
group_names = ['Group A', 'Group B', 'Group C', 'Group D', 'Group E', 'Group F', 'Group G', 'Group H']

for idx, table in enumerate(tables):
    group_name = group_names[idx]  # Assigning group names based on their position in the tables list

    for row in table.find_all('tr')[1:]:
        player_count += 1
        columns = row.find_all(['th', 'td'])
        position_raw = columns[1].text.strip()
        position = ''.join([char for char in position_raw if not char.isdigit()]).strip()
        if len(columns) < 7:
            continue  # Skip processing this player if data is incomplete

        anchor_tag = columns[2].find('a')
        if anchor_tag is None:
            player_name = 'N/A'
        else:
            player_name = anchor_tag.text.strip()

        date_of_birth = columns[3].text.strip()

        try:
            age = int(date_of_birth[date_of_birth.rfind('(') + 5: -1])
        except ValueError:
            age = 'Unknown'

        club = columns[6].text.strip()

        print(f"Number: {player_count}, Group: {group_name}, Position: {position}, Player Name: {player_name}, Age: {age}, Club: {club}")