import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from datetime import datetime

# Get the HTML content of the Wikipedia page
NO_IMAGE = 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/No-image-available.png/480px-No-image-available.png'
url = "https://en.wikipedia.org/wiki/List_of_association_football_stadiums_by_capacity"
response = requests.get(url)
html = response.text

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Find the table containing the stadium data
table = soup.find_all("table", {"class":'wikitable sortable'})[0]
table_rows = table.find_all('tr')

def clean_text(text):
    text = str(text).strip()
    if text.find(' ♦'):
        text = text.split(' ♦')[0]
    if text.find('[') != -1:
        text = text.split('[')[0]
    if text.find(' (formerly)') != -1:
        text = text.split(' (formerly)')[0]

    return text.replace('\n', '')

# Extract the stadium data into a list of dictionaries
data = []
for i in range(1, len(table_rows)):
    tds = table_rows[i].find_all('td')
    values = {
        'rank': i,
        'stadium': clean_text(tds[0].text),
        'capacity': clean_text(tds[1].text).replace(',', '').replace('.', ''),
        'region': clean_text(tds[2].text),
        'country': clean_text(tds[3].text),
        'city': clean_text(tds[4].text),
        'images': 'https://' + tds[5].find('img').get('src').split("//")[1] if tds[5].find('img') else "NO_IMAGE",
        'home_team': clean_text(tds[6].text),
    }
    data.append(values)

# Convert the list of dictionaries into a Pandas DataFrame
stadium_df = pd.DataFrame(data)

# Clean the DataFrame data
stadium_df['images'] = stadium_df['images'].apply(lambda x : x if x not in ['NO_IMAGE', '', None] else NO_IMAGE)
stadium_df['capacity'] = stadium_df['capacity'].astype(int)

# Save the DataFrame to a CSV file
file_name = ('stadium_clean.csv')
stadium_df.to_csv('data/'+ file_name, index=False)