import os
import csv
from bs4 import BeautifulSoup
from tm_lists import league_code_defs

# Functions to format data to desired format
def format_num(num):
    if num == "-":
        return None
    else:
        return int("".join(num.split(".")))

def format_percent(pct_str):
    pct_num = pct_str.split(" ")[0]
    if pct_num:
        return float(pct_num)
    else:
        return None


# Open file to store data
f = open("../../csv-data/stadium_data.csv", "w", encoding="utf-8", newline='')
writer = csv.writer(f)

# Write data headers
column_headers = ["Country", "League", "Year", "Stadium", "Club", "Stadium Capacity", "Season Total Spectators", "Season Average", "Total Matches", "Sold Out", "Average Attendance Percentage"]
writer.writerow(column_headers)

# Set directory and loop through all files therein
directory = "./stadium-pages"
for filename in os.listdir(directory):

    # Get some metadata from filename using league code definitions from tm_lists
    filename_data = filename[:-5].split("-")
    year = filename_data[2]
    league_code = filename_data[1]
    country = league_code_defs[league_code]["country"]
    league = league_code_defs[league_code]["league"]

    # Create path for file and if file exists, open to read
    path = os.path.join(directory, filename)
    if os.path.isfile(path):
        with open(path, "r", encoding="utf-8") as fp:
                
                # Parse with Beautiful Soup, going through each row in the page's table
                soup = BeautifulSoup(fp, 'html.parser')
                rows = soup.find_all("tr", {"class": ["odd", "even"]})
                
                for row in rows:
                    # Get a list of only the text for each row
                    text = row.find_all(text=True)
                    
                    # Assign column text to variables, formatting where necessary
                    stadium = text[2]
                    club = text[3]
                    capacity = format_num(text[4])
                    season_tot = format_num(text[5])
                    season_avg = format_num(text[6])
                    matches = format_num(text[7])
                    sold_out = format_num(text[8])
                    season_avg_percent = format_percent(text[9])
                    
                    # Create list of data with above variables, write as row to CSV
                    row = [country, league, year, stadium, club, capacity, season_tot, season_avg, matches, sold_out, season_avg_percent]
                    writer.writerow(row)

# Close csv
f.close()