import requests
from bs4 import BeautifulSoup

url = 'https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads'

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find the table containing the player data
table = soup.find('table', class_='sortable')

# Iterate through each row in the table
for row in table.find_all('tr')[1:]:
    # Extract data from each column in the row
    columns = row.find_all(['th', 'td'])

    # Extract player name, age, team, and position
    player_name = columns[2].text.strip()
    age = columns[3].text.strip()[1:-1]  # Remove parentheses and age number
    team = columns[6].text.strip()
    position = columns[1].text.strip().split()[0]  # Remove number from position

    # Print the extracted data
    print(f"Player: {player_name}, Age: {age}, Team: {team}, Position: {position}")