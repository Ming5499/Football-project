import requests
from bs4 import BeautifulSoup

def  get_wikipedia_page(url):
    print("Getting page...",url)
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status() #check if the request is successful
        return response.text
    except requests.RequestException as e:
        print(f"Error: {e}")
        
        
def get_wikipedia_data(html):
    soup = BeautifulSoup(html,'html.parser')