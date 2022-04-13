import os
import csv
from bs4 import BeautifulSoup
from helpers import league_code_defs

# Open file to store data
f = open("../../csv-data/league_table_data.csv", "w", encoding="utf-8", newline='')
writer = csv.writer(f)

# Write data headers
column_headers = ["Country", "League", "Year", "Position", "Club", "Points", "Goal Differential"]
writer.writerow(column_headers)

# Set directory and loop through all files therein
directory = "./table-pages"


for filename in os.listdir(directory):
    # Print which file is being processed to show progress
    print("Processing:", filename)

    # Get some metadata from filename using league code definitions from helpers
    filename_data = filename[:-5].split("-")
    year = filename_data[2]
    league_code = filename_data[1]
    country = league_code_defs[league_code]["country"]
    league = league_code_defs[league_code]["league"]


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
                club = columns[2].find("a").get("title")
                goal_diff = columns[8].getText()
                points = columns[9].getText()
                print(position, club, goal_diff, points)

                # Create list of data using above variables, write as row to CSV
                row = [country, league, year, position, club, points, goal_diff]
                writer.writerow(row)

# Close csv
f.close()