import os
import csv
from bs4 import BeautifulSoup
from helpers import league_code_defs, season_conversion

# Open file to store data
f = open("../../csv-data/multitier_table_data.csv", "w", encoding="utf-8", newline='')
writer = csv.writer(f)

# Write data headers
column_headers = [
    "Country", 
    "League", 
    "Tier", 
    "Size", 
    "Start Year", 
    "Season", 
    "Club", 
    "Position",
    "Overall Position",
]
writer.writerow(column_headers)

# Set directory and loop through all files therein
directory = "./multitier-pages"


for filename in os.listdir(directory):
    # Print which file is being processed to show progress
    print("Processing:", filename)

    # Get some metadata from filename using league code definitions from helpers
    filename_data = filename[:-5].split("-")
    start_year = filename_data[2]
    season = season_conversion[int(start_year)]
    league_code = filename_data[1]
    country = league_code_defs[league_code]["country"]
    league = league_code_defs[league_code]["league"]
    tier = league_code_defs[league_code]["tier"]
    size = league_code_defs[league_code]["size"]

    tier1_size = league_code_defs[f"{league_code[:-1]}1"]["size"]


    # Create path for file and if file exists, open to read
    path = os.path.join(directory, filename)
    if os.path.isfile(path):
        with open(path, "r", encoding="utf-8") as fp:
            
            # Use HTML parsing with Beautiful Soup
            soup = BeautifulSoup(fp, 'html.parser')

            # Find relevant table
            table = soup.find_all("tbody")[1]
            rows = table.find_all("tr")

            # Loop through table rows
            for row in rows:
                # Get table columns
                columns = row.find_all("td")
                # Assign column data to variables
                position = columns[0].getText().strip()
                if tier == 1:
                    overall_position = position
                else:
                    overall_position = str(int(tier1_size) + int(position))

                club = columns[2].find("a").get("title")
                goal_diff = columns[8].getText()
                points = columns[9].getText()

                # Create list of data using above variables, write as row to CSV
                row = [country, league, tier, size, start_year, season,  club, position, overall_position]
                writer.writerow(row)

# Close csv
f.close()

