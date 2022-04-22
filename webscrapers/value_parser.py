import os
import csv
from bs4 import BeautifulSoup
from helpers import league_code_defs, parse_fee

# Open file to store data
f = open("../../csv-data/squad_value_data.csv", "w", encoding="utf-8", newline='')
writer = csv.writer(f)

# Write data headers
column_headers = ["Country", "League", "Year", "Club", "Squad Size", "Average Age", "Foreigners", "Market Value per Player", "Total Market Value"]
writer.writerow(column_headers)

# Set directory and loop through all files therein
directory = "./value-pages"


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
                club = columns[1].find("a").get("title")
                squad = columns[2].getText()
                age = columns[3].getText()
                foreigners = columns[4].getText()
                avg_val = parse_fee(columns[5].getText())
                tot_val = parse_fee(columns[6].getText())
                print(club, squad, age, foreigners, avg_val, tot_val)

                # Create list of data using above variables, write as row to CSV
                row = [country, league, year, club, squad, age, foreigners, avg_val, tot_val]
                writer.writerow(row)

# Close csv
f.close()