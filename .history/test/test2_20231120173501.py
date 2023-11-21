import requests
from bs4 import BeautifulSoup

# List of country URLs
country_urls = [
    'https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads#Ecuador',
    'https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads#Senegal',
    'https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads#Netherlands'
]

# Iterate through the list of country URLs
for country_url in country_urls:
    # Send a GET request to the current country URL
    response = requests.get(country_url)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table containing the player data
    table = soup.find('table', class_='sortable')

    # Extract player data from each row
    for row in table.find_all('tr')[1:]:
        # Extract data from each column in the row
        columns = row.find_all(['th', 'td'])

        # Extract player information
        player_name = columns[2].find('a').text.strip()
        team = columns[6].text.strip()
        position = columns[1].text.strip()
        age = columns[3].text.strip()

        # Print the extracted data
        print(f"Country: {country_url.split('#')[-1]}, Player: {player_name}, Age: {age}, Team: {team}, Position: {position}")
