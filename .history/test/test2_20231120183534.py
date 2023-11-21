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
    tables = soup.find_all('table', class_='sortable')

    # Extract country name from the table header
    country_name = soup.find('span', {'id': group}).text.strip()
    
    # Find the correct table associated with the group
    table = None
    for t in tables:
        if country_name in str(t):  # Look for the country name within the table
            table = t
            break
    
    if table:
        for row in table.find_all('tr')[1:]:
            # Extract data from each column in the row
            columns = row.find_all(['th', 'td'])
            # (rest of your code remains the same)
            # Print the extracted data along with the group, country name, and other details
            print(f"Number: {number}, Position: {position}, Player Name: {player_name}, Age: {age}, Club: {club}, Group: {group.split('_')[-1]}, Country: {country_name}")
    else:
        print(f"Table not found for {group}")

