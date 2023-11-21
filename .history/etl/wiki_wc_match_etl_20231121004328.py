import pandas as pd
from bs4 import BeautifulSoup
import requests


years = [1930, 1934, 1938, 1950, 1954, 1958, 1962, 1966, 1970, 1974,
         1978, 1982, 1986, 1990, 1994, 1998, 2002, 2006, 2010, 2014,
         2018, 2022]


def get_matches(year):
    url = f'https://en.wikipedia.org/wiki/{year}_FIFA_World_Cup'
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    matches = soup.find_all('div', class_='footballbox')

    home = []
    score = []
    away = []

    for match in matches:
        home.append(match.find('th', class_='fhome').get_text())
        score.append(match.find('th', class_='fscore').get_text())
        away.append(match.find('th', class_='faway').get_text())

    dict_football = {'home': home, 'score': score, 'away': away}
    df_football = pd.DataFrame(dict_football)
    df_football['year'] = year
    
    return df_football



match = [get_matches(year) for year in years]
df_match = pd.concat(match, ignore_index=True)
df_match.to_csv("data/world_cup_match.csv", index=False)


