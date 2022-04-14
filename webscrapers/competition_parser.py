import os
import csv
from bs4 import BeautifulSoup
from helpers import land_id_defs, comp_code_defs

# Open file to store data
f = open("../../csv-data/int_competition_data.csv", "w", encoding="utf-8", newline='')
writer = csv.writer(f)

# Write data headers
column_headers = ["Country", "League", "Year", "Competition", "Round of 16", "Quarter Finals", "Semi Finals", "Finals", "Win", "Points"]
writer.writerow(column_headers)

# Set directory and loop through all files therein
directory = "./competition-pages"

def calc_points(comp_code, ro16, qf, sf, f, v):
    points = None
    if comp_code == "CL":
        points = ro16*96 + qf*106 + sf*125 + f*155 + v*200
    if comp_code == "EL":
        points = ro16*12 + qf*18 + sf*28 + f*46 + v*86
    return points


for filename in os.listdir(directory):
    # Print which file is being processed to show progress
    print("Processing:", filename)

    # Get some metadata from filename using league code definitions from helpers
    filename_data = filename[:-5].split("-")
    comp_code = filename_data[1]
    land_id = filename_data[2]

    country = land_id_defs[land_id]["country"]
    league = land_id_defs[land_id]["league"]
    competition = comp_code_defs[comp_code]


    # Create path for file and if file exists, open to read
    path = os.path.join(directory, filename)
    if os.path.isfile(path):
        with open(path, "r", encoding="utf-8") as fp:
            
            # Use HTML parsing with Beautiful Soup
            soup = BeautifulSoup(fp, 'html.parser')

            # Find relevant table
            table = soup.find_all("tbody")[1]
            rows = table.find_all("tr")[:17]

            # Loop through table rows
            for row in rows:
                # Get table columns
                columns = row.find_all("td")

                # Assign column data to variables
                year = columns[0].getText()

                # TODO: Write this more concisely
                if comp_code == "CL":
                    results = [len(col("a")) for col in columns[3:8]]
                elif comp_code == "EL":
                    results = [len(col("a")) for col in columns[4:9]]

                ro16, qf, sf, f, v = results

                points = calc_points(comp_code, ro16, qf, sf, f, v)

                # Print row data
                print(country, league, year, competition, ro16, qf, sf, f, v, points)

                # Create row list and write to csv
                row = [country, league, year, competition, ro16, qf, sf, f, v, points]
                writer.writerow(row)