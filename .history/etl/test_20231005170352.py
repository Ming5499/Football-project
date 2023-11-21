import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from datetime import datetime

NO_IMAGE = 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/No-image-available.png/480px-No-image-available.png'

def get_wikipedia_page(url):
    print("Getting page...", url)
    try:
        response = requests.get(url, timeout=10)
        return response.text
    except requests.RequestException as e:
        print(f"Error: {e}")

def get_wikipedia_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find_all("table", {"class": 'wikitable sortable'})[0]
    table_rows = table.find_all('tr')
    return table_rows

def clean_text(text):
    text = str(text).strip()
    if text.find(' ♦'):
        text = text.split(' ♦')[0]
    if text.find('[') != -1:
        text = text.split('[')[0]
    if text.find(' (formerly)') != -1:
        text = text.split(' (formerly)')[0]
    return text.replace('\n', '')

url = "https://en.wikipedia.org/wiki/List_of_association_football_stadiums_by_capacity"
html = get_wikipedia_page(url)
rows = get_wikipedia_data(html)
data = []

for i in range(1, len(rows)):
    tds = rows[i].find_all('td')
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

json_rows = json.dumps(data)

data = kwargs['taskid'].xcom_pull(key='rows', task_ids='extract_data_from_wikipedia')
data = json.loads(data)
stadium_df = pd.DataFrame(data)
stadium_df['image'] = stadium_df['image'].apply(lambda x: x if x not in ['NO_IMAGE', '', None] else NO_IMAGE)
stadium_df['capacity'] = stadium_df['capacity'].astype(int)

data = kwargs['taskid'].xcom_pull(key='rows', task_ids='transform_wikipedia_data')
data = json.loads(data)
data = pd.DataFrame(data)
file_name = ('stadium_clean_' + str(datetime.now()) + '.csv')
data.to_csv('data/' + file_name, index=False)
