import requests
from bs4 import BeautifulSoup

url = 'https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads'

# List of groups from A to H
groups = ['Group_A']

player_count = 0  # Initialize player count

for group in groups:
    # Extract country name from the table header row for the first player
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    tables = soup.find_all('table', class_='sortable')
    for table in tables:
        row = table.find_all('tr')[1]

        # Extract player data from the current row
        for row in table.find_all('tr')[2:]:
            player_count += 1  # Increment player count for each player

            columns = row.find_all(['th', 'td'])
            number = str(player_count)  # Assign player number based on count
            position_raw = columns[1].text.strip()
            position = ''.join([char for char in position_raw if not char.isdigit()]).strip()
            
            # Check if the anchor tag exists before accessing its text
            player_anchor = columns[2].find('a')
            player_name = player_anchor.text.strip() if player_anchor else "N/A"
            
            date_of_birth = columns[3].text.strip()
            age = int(date_of_birth[date_of_birth.rfind('(') + 5: -1])
            club = columns[6].text.strip()

            # Print the extracted data along with the group, country name, and other details
            print(f"Number: {number}, Position: {position}, Player Name: {player_name}, Age: {age}, Club: {club}, Group: {group.split('_')[-1]}")
