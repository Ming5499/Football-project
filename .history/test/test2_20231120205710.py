import requests
from bs4 import BeautifulSoup

url = 'https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads'

player_count = 0  # Initialize player count
player_data = []  # List to store player data

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
tables = soup.find_all('table', class_='sortable')

group_names = {}  # Dictionary to store group names and their respective rows

for table in tables:
    group_header = table.find_previous('h3')  # Get the group name from the preceding h3 header
    group_name = group_header.text.strip() if group_header else "Unknown Group"

    group_identifier = group_name.split(' ')[-1][:-6]  # Extracting only the group identifier (A, B, C, etc.)

    group_names[group_identifier] = []

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

        group_names[group_identifier].append({
            "Group": group_identifier,
            "Number": player_count,  # Include the player count
            "Position": position,
            "Player Name": player_name,
            "Age": age,
            "Club": club
        })

# Printing results for demonstration purposes
for group, players in group_names.items():
    for player in players:
        print(f"Number: {player['Number']}, Group: {player['Group']}, Position: {player['Position']}, Player Name: {player['Player Name']}, Age: {player['Age']}, Club: {player['Club']}")
