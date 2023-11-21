import requests
from bs4 import BeautifulSoup
import pandas as pd
import json


# Get the HTML content of the Wikipedia page
NO_IMAGE = 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/No-image-available.png/480px-No-image-available.png'
url = "https://en.wikipedia.org/wiki/List_of_European_stadiums_by_capacity"
response = requests.get(url)
html = response.text

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Find the table containing the stadium data
table = soup.find_all("table", {"class":'wikitable sortable'})[0]
table_rows = table.find_all('tr')
span = soup.find_all("span", {"class":'mw-headline'})[0]
span_rows = table.find_all('tr')

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
for span in soup.find_all("span", {"class":'mw-headline'})[0]:
    span_rows = table.find_all('id')

    data = []
    for row in table_rows[1:]:  # Start from index 1 to skip the header row
        tds = row.find_all('td')
        if len(tds) >= 6:  # Ensure there are enough columns to extract data
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
stadium_df.to_csv('data/stadium_clean3.csv', index=False)