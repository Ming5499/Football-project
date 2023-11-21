import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

def  get_wikipedia_page(url):
    print("Getting page...",url)
    try:
        #fetch the HTML content
        response = requests.get(url, timeout=10)
        return response.text
    except requests.RequestException as e:
        print(f"Error: {e}")
        
        
def get_wikipedia_data(html):
    soup = BeautifulSoup(html,'html.parser')
    table = soup.find_all("table",{"class":'wikitable sortable'})[0]
    table_rows = table.find_all('tr')
    
    return table_rows

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

#having all pipepline step to executed
def extract_wikipedia_data(**kwargs):
    url = kwargs['url']
    html = get_wikipedia_data(url)
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
        
    #converts the list of dictionaries into a JSON format
    json_rows = json.dumps(data)
    #push the JSON data into the Airflow context
    kwargs['ti'].xcom_push(key='rows', value=json_rows)

    return "OK"

def transform_wikipedia_data(**kwargs):
    #pull the rows XCom and load the data into a database.
    rows = kwargs['ti'].xcom_pull(key='rows', task_ids='extract_data_from_wikipedia')