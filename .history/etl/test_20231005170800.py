import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from datetime import datetime

# Get the HTML content of the Wikipedia page
url = "https://en.wikipedia.org/wiki/List_of_largest_stadiums_in_the_world"
response = requests.get(url)
html = response.text

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Find the table containing the stadium data
table = soup.find_all("table", {"class":'wikitable sortable'})[0]
table_rows = table.find_all('tr')

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
stadium_df['image'] = stadium_df['image'].apply(lambda x : x if x not in ['NO_IMAGE', '', None] else NO_IMAGE)
stadium_df['capicity'] = stadium_df['capicity'].astype(int)

# Save the DataFrame to a CSV file
file_name = ('stadium_clean_' + str(datetime.now()) + '.csv')
stadium_df.to_csv('data/'+ file_name, index=False)