import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://en.wikipedia.org/wiki/List_of_association_football_stadiums_by_capacity'
def clean_text(text):
    text = str(text).strip()
    text = text.replace('&nbsp', '')
    if text.find(' ♦'):
        text = text.split(' ♦')[0]
    if text.find('[') != -1:
        text = text.split('[')[0]
    if text.find(' (formerly)') != -1:
        text = text.split(' (formerly)')[0]

    return text.replace('\n', '')
print("Getting page...", url)
try:
    response = requests.get(url, timeout=10)
    html = response.text
except requests.RequestException as e:
    print(f"Error: {e}")
    html = None

if html:
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find_all("table", {"class": 'wikitable sortable'})[0]
    table_rows = table.find_all('tr')

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

    data_df = pd.DataFrame(data)
    data_df.to_csv("data/output_clean.csv", index=False)
