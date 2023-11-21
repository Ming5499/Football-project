import requests
from bs4 import BeautifulSoup

url = "https://en.wikipedia.org/wiki/List_of_association_football_stadiums_by_capacity"

# Make a request to the website
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Extract the table containing the list of stadiums
table = soup.find("table", class_="wikitable sortable")

# Create a list to store the stadium data
stadiums = []

# Iterate over the rows in the table
for row in table.find_all("tr"):
    # Skip the header row
    if not row.find("td", class_="Rank").text:
        continue

    # Extract the stadium rank, name, seating capacity, region, country, city, images, and home team(s)
    stadium_rank = row.find("td", class_="Rank").text
    stadium_name = row.find("td", class_="Stadium").text
    seating_capacity = row.find("td", class_="Seating_capacity").text
    region = row.find("td", class_="Region").text
    country = row.find("td", class_="Country").text
    city = row.find("td", class_="City").text
    images = row.find("td", class_="Images").text
    home_teams = row.find("td", class_="Home_team(s)").text

    # Create a dictionary to store the stadium data
    stadium = {
        "rank": stadium_rank,
        "name": stadium_name,
        "seating_capacity": seating_capacity,
        "region": region,
        "country": country,
        "city": city,
        "images": images,
        "home_teams": home_teams,
    }

    # Add the stadium to the list
    stadiums.append(stadium)

# Print the list of stadiums
for stadium in stadiums:
    print(stadium)