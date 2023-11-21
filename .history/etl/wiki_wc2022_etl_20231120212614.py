import csv
import requests
from bs4 import BeautifulSoup

def get_wikipedia_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request is successful
        return response.content
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

def extract_player_data(soup):
    player_count = 0
    group_names = {}

    tables = soup.find_all('table', class_='sortable')

    for table in tables:
        group_header = table.find_previous('h3')
        group_name = group_header.text.strip() if group_header else "Unknown Group"
        group_identifier = group_name.split(' ')[-1][:-6]
        group_names[group_identifier] = []

        for row in table.find_all('tr')[1:]:
            player_count += 1
            columns = row.find_all(['th', 'td'])
            position_raw = columns[1].text.strip()
            position = ''.join([char for char in position_raw if not char.isdigit()]).strip()

            if len(columns) < 7:
                continue  # Skip incomplete player data

            anchor_tag = columns[2].find('a')
            player_name = anchor_tag.text.strip() if anchor_tag else 'N/A'

            date_of_birth = columns[3].text.strip()
            # try:
            #     age = int(date_of_birth[date_of_birth.rfind('(') + 5: -1])
            # except ValueError:
            #     age = 'Unknown'
            age = columns[3].text.strip()
            club = columns[6].text.strip()

            group_names[group_identifier].append({
                "Group": group_identifier,
                "Number": player_count,
                "Position": position,
                "Player Name": player_name,
                "Age": age,
                "Club": club
            })

    return group_names

def transform_player_data(group_data):
    for group, players in group_data.items():
        for player in players:
            date_of_birth = player['Age']  # 'Age' here holds the date of birth info

            # Extracting age from the date of birth
            try:
                birth_year = int(date_of_birth[date_of_birth.rfind('(') + 1: date_of_birth.rfind(')')])
                current_year = datetime.now().year
                age = current_year - birth_year
                player['Age'] = age  # Update the 'Age' field with the calculated age
            except (ValueError, IndexError):
                player['Age'] = 'Unknown'

    return group_data



def write_to_csv(data, file_name):
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['Number', 'Player Name', 'Nation', 'Position', 'Age', 'Club']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        writer.writeheader()
        for group, players in data.items():
            for player in players:
                writer.writerow({
                    'Number': player['Number'],
                    'Player Name': player['Player Name'],
                    'Nation': player['Group'],
                    'Position': player['Position'],
                    'Age': player['Age'],
                    'Club': player['Club']
                })

    print(f"Data has been saved to {file_name}")

def scrape_and_save_data(url, file_name):
    html_content = get_wikipedia_page(url)
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        player_data = extract_player_data(soup)
        write_to_csv(player_data, file_name)

# Call the function to perform the scraping and save the data to a CSV file
url = 'https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads'
file_name = "FIFA_World_Cup_2022_players.csv"

scrape_and_save_data(url, file_name)
