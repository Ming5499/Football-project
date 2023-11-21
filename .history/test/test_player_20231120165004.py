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
    player_name = columns[2].text.strip()
    team = columns[1].text.strip()
    position = columns[5].text.strip()
    
    # Print the extracted data (you can process or store it as needed)
    print(f"Player: {player_name}, Team: {team}, Position: {position}")
