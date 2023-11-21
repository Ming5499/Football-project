import requests
from bs4 import BeautifulSoup
import pandas as pd
import json


NO_IMAGE = 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/No-image-available.png/480px-No-image-available.png'






# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Find the table containing the stadium data
table = soup.find_all("table", {"class":'wikitable sortable'})

span = soup.find_all("span", {"class":'mw-headline'})


def clean_text(text):
    text = str(text).strip()
    if text.find(' ♦'):
        text = text.split(' ♦')[0]
    if text.find('[') != -1:
        text = text.split('[')[0]
    if text.find(' (formerly)') != -1:
        text = text.split(' (formerly)')[0]

    return text.replace('\n', '')

def extract_wikipedia_data(url):
    location = ['African','Asia','European','North American','Oceanian','South American']
    url = f"https://en.wikipedia.org/wiki/List_of_{location}_stadiums_by_capacity"
    # Get the HTML content of the Wikipedia page
    response = requests.get(url)
    html = response.text
    data = []
    for locations in location:
        for a in range(1,4):
            table_rows = table[a].find_all('tr')
            
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
stadium_df.to_csv('data/stadium_clean4.csv', index=False)