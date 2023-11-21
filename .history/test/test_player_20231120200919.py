import requests
from bs4 import BeautifulSoup
import csv

url = 'https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads'

# List of groups from A to H
groups = ['Group_A']

player_data = []  # List to store player data

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
            
            # Check if the date of birth has the expected format
            age = int(date_of_birth[date_of_birth.rfind('(') + 5: -1]) if '(' in date_of_birth else 0
            
            club = columns[6].text.strip()

            # Append the extracted data to player_data list
            player_data.append({
                "Number": number,
                "Position": position,
                "Player Name": player_name,
                "Age": age,
                "Club": club,
                "Group": group.split('_')[-1]
            })

# Write the extracted data to a CSV file
csv_file = 'player_data.csv'
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    fieldnames = ['Number', 'Position', 'Player Name', 'Age', 'Club', 'Group']
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    for player in player_data:
        writer.writerow(player)
        # Print the extracted data
        print(f"Number: {player['Number']}, Position: {player['Position']}, Player Name: {player['Player Name']}, Age: {player['Age']}, Club: {player['Club']}, Group: {player['Group']}")

print(f"Data has been written to {csv_file}")
