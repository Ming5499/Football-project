import requests
from bs4 import BeautifulSoup
import pandas as pd
import json


# Get the HTML content of the Wikipedia page
NO_IMAGE = 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/No-image-available.png/480px-No-image-available.png'
url = "https://en.wikipedia.org/wiki/List_of_African_stadiums_by_capacity"
response = requests.get(url)
html = response.text

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')



def clean_text(text):
    text = str(text).strip()
    if text.find(' ♦'):
        text = text.split(' ♦')[0]
    if text.find('[') != -1:
        text = text.split('[')[0]
    if text.find(' (formerly)') != -1:
        text = text.split(' (formerly)')[0]

    return text.replace('\n', '')

data = []
for i in range(0,7):
    table = soup.find_all("table", {"class":'wikitable sortable'})[i]
    table_rows = table.find_all('tr')
    for i in range(1, len(table_rows)):
        
        tds = table_rows[i].find_all('td')
        values = {
            'name': clean_text(tds[0].text),
            'seating capacity': clean_text(tds[1].text),
            'city': clean_text(tds[2].text),
            'country': clean_text(tds[3].text),
            'build': clean_text(tds[4].text),
            'images': 'https://' + tds[5].find('img').get('src').split("//")[1] if tds[5].find('img') else NO_IMAGE,
        }
        data.append(values)
        


# Convert the list of dictionaries into a Pandas DataFrame
stadium_df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
stadium_df.to_csv('data/stadium_4.csv', index=False)