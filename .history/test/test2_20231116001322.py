import requests

# Replace YOUR_API_KEY with your actual API key
api_key = 'ff8c5fd6e8msh53942da5870f9cbp1836f0jsn2adaf10f8328'

# Set the API URL and headers
api_url = 'https://api-football-v1.p.rapidapi.com/countries'
headers = {
    'X-Auth-Token': api_key
}

# Send the GET request to the API
response = requests.get(api_url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON data
    data = response.json()

    # Print the fixtures
    for fixture in data['fixtures']:
        print(fixture)
else:
    print('Error:', response.status_code)