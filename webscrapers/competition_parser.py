import os
import csv
from bs4 import BeautifulSoup
from helpers import land_id_defs, comp_code_defs

# Open file to store data
f = open("../../csv-data/int_competition_data.csv", "w", encoding="utf-8", newline='')
writer = csv.writer(f)

# Write data headers
column_headers = [
    "Country", 
    "League", 
    "Year", 
    "Champions League Round of 16", # CL = [3:8]
    "Champions League Quarter Finals", 
    "Champions League Semi Finals", 
    "Champions League Finals", 
    "Champions League Win", 
    "Europa League Round of 16", # EL = [8:13]
    "Europa League Quarter Finals", 
    "Europa League Semi Finals", 
    "Europa League Finals", 
    "Europa League Win", 
    "Points"
]
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

items = {}

for filename in os.listdir(directory):
    # Print which file is being processed to show progress
    print("Processing:", filename)

    # Get some metadata from filename using league code definitions from helpers
    filename_data = filename[:-5].split("-")
    comp_code = filename_data[1]
    land_id = filename_data[2]

    country = land_id_defs[land_id]["country"]
    league = land_id_defs[land_id]["league"]


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

                item_name = f"{country}{year[:2]}"
                if item_name not in items:
                    items[item_name] = [None] * 14
                    items[item_name][0] = country
                    items[item_name][1] = league
                    items[item_name][2] = f"20{year[:2]}"
                    items[item_name][13] = 0
    
                if comp_code == "CL":
                    ro16, qf, sf, f, w = [len(col("a")) for col in columns[3:8]]
                    points = calc_points(comp_code, ro16, qf, sf, f, w)
                    items[item_name][3] = ro16
                    items[item_name][4] = qf
                    items[item_name][5] = sf
                    items[item_name][6] = f
                    items[item_name][7] = w
                    items[item_name][13] += points
                elif comp_code == "EL":
                    ro16, qf, sf, f, w = [len(col("a")) for col in columns[4:9]]
                    points = calc_points(comp_code, ro16, qf, sf, f, w)
                    items[item_name][8] = ro16
                    items[item_name][9] = qf
                    items[item_name][10] = sf
                    items[item_name][11] = f
                    items[item_name][12] = w
                    items[item_name][13] += points

                # Print row data
                print(items[item_name])

# Iterate throgh dict and write each item to CSV
for item in items.values():
    writer.writerow(item)