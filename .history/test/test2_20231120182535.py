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

    # Find the header for the country section
    

    for h3 in soup.find_all('h3'):
        country_name = h3.find('span', class_='mw-headline').text.strip()
        print(country_name)
    # print(f"Group: {group.split('_')[-1]}")  # Print the group name

    # Find the table containing the player data
    table = soup.find('table', class_='sortable')

   
    for row in table.find_all('tr')[1:]:
        # Extract data from each column in the row
        columns = row.find_all(['th', 'td'])
        number = columns[0].text.strip()
        position_raw = columns[1].text.strip()
        # Extract position without the number, handling variations in format
        position = ''.join([char for char in position_raw if not char.isdigit()]).strip()
        player_name = columns[2].find('a').text.strip()
        date_of_birth = columns[3].text.strip()
        # Extract age as integer from the date of birth
        age = int(date_of_birth[date_of_birth.rfind('(') + 5: -1])
        club = columns[6].text.strip()
        
        # Print the extracted data along with the group, country name, and other details
        # print(f"Number: {number}, Position: {position}, Player Name: {player_name}, Age: {age}, Club: {club}, Group: {group.split('_')[-1]}, Country: {country_name}")

    
