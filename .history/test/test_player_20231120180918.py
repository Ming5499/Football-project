import requests
from bs4 import BeautifulSoup

base_url = 'https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads'

# List of groups from A to H
groups = ['Group_A', 'Group_B', 'Group_C', 'Group_D', 'Group_E', 'Group_F', 'Group_G', 'Group_H']

for group in groups:
    url = f'{base_url}#{group}'  # URL for each group

    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table containing the player data
    table = soup.find('table', class_='sortable')

    if table:
        print(f"Group: {group.split('_')[-1]}")  # Print the group name

        # Iterate through each row in the table
        for row in table.find_all('tr')[1:]:
            # Extract data from each column in the row
            columns = row.find_all(['th', 'td'])
            number = columns[0].text.strip()
            position_raw = columns[1].text.strip()
            # Extract position without the number, handling variations in format
            position = ''.join([char for char in position_raw if not char.isdigit()]).strip()
            player_name = columns[2].find('a').text.strip()

            # Retrieve country name for the player using a country data API or other source
            country_name = get_country_name(player_name)  # Replace this with actual country name retrieval logic

            # Extract remaining data from other columns
            date_of_birth = columns[3].text.strip()
            age = int(date_of_birth[date_of_birth.rfind('(') + 5: -1])
            club = columns[6].text.strip()

            # Print the extracted data along with the group, country name, and other details
            print(
                f"Number: {number}, Position: {position}, Player Name: {player_name}, Age: {age}, Club: {club}, Group: {group.split('_')[-1]}, Country: {country_name}"
            )

    else:
        print(f"No data found for {group}.")
