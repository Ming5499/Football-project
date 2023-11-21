import requests
from bs4 import BeautifulSoup

base_url = 'https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads'

# List of groups from A to H
groups = ['Group_A']

country_names = []

processed_tables = set()

for group in groups:
    # Extract country name from the table header row for the first player
    group_data_extracted = False
    url = f'{base_url}#{group}'  # URL for each group
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    tables = soup.find_all('table', class_='sortable')
    for table in tables:
        row = table.find_all('tr')[1]

        if not group_data_extracted:
            country_names.append(row.find_all('td')[0].text.strip())
            group_data_extracted = True

        # Extract player data from the current row
        if table not in processed_tables:
            for row in table.find_all('tr')[2:]:
                columns = row.find_all(['th', 'td'])
                number = columns[0].text.strip()
                position_raw = columns[1].text.strip()
                position = ''.join([char for char in position_raw if not char.isdigit()]).strip()
                player_name = columns[2].find('a').text.strip()
                date_of_birth = columns[3].text.strip()
                age = int(date_of_birth[date_of_birth.rfind('(') + 5: -1])
                club = columns[6].text.strip()

                # Print the extracted data along with the group, country name, and other details
                print(f"Number: {number}, Position: {position}, Player Name: {player_name}, Age: {age}, Club: {club}, Group: {group.split('_')[-1]}")

            processed_tables.add(table)
