import requests
from bs4 import BeautifulSoup
import pandas as pd
import json


# Get the HTML content of the Wikipedia page
response = requests.get('https://en.wikipedia.org/wiki/List_of_European_stadiums_by_capacity')
html = response.text

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Find the table containing the stadium data
table = soup.find_all('table', {'class': 'wikitable sortable'})[0]
table_rows = table.find_all('tr')

# Extract the stadium data into a list of dictionaries
data = []
for i in range(1, len(table_rows)):
    tds = table_rows[i].find_all('td')
    values = {
        'rank': i,
        'name': tds[0].text.strip(),
        'seating capacity': clean_text(tds[1].text),
        'city': tds[2].text.strip(),
        'country': tds[3].text.strip(),
        'build': clean_text(tds[4].text),
        'images': 'https://' + tds[5].find('img').get('src').split("//")[1] if tds[5].find('img') else 'NO_IMAGE',
    }
    data.append(values)

# Convert the list of dictionaries into a Pandas DataFrame
stadium_df = pd.DataFrame(data)

# Clean the DataFrame data
stadium_df['images'] = stadium_df['images'].apply(lambda x: x if x not in ['NO_IMAGE', '', None] else 'NO_IMAGE')


# Save the DataFrame to a CSV file
stadium_df.to_csv('data/stadium_clean4.csv', index=False)