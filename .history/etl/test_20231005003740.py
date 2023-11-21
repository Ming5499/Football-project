import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://en.wikipedia.org/wiki/List_of_association_football_stadiums_by_capacity'

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

    for i in range(1, len(table_rows)):
        tds = table_rows[i].find_all('td')
        values = {
            'rank': i,
            'stadium': tds[0].text,
            'capacity': tds[1].text,
            'region': tds[2].text,
            'country': tds[3].text,
            'city': tds[4].text,
            'images': tds[5].find('img').get('src').split("//")[1] if tds[5].find('img') else "NO_IMAGE",
            'home_team': tds[6].text,
        }
        data.append(values)

    data_df = pd.DataFrame(data)
    data_df.to_csv("data/output.csv", index=False)
