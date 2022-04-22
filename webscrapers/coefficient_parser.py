import os
import csv
from bs4 import BeautifulSoup

# Open file to store data
f = open("../../csv-data/coefficient_data.csv", "w", encoding="utf-8", newline='')
writer = csv.writer(f)

# Write data headers
column_headers = ["Year", "Country", "Rank", "Points"]
writer.writerow(column_headers)

# Set directory and loop through all files therein
directory = "./coefficient-pages"


for filename in os.listdir(directory):
    # Print which file is being processed to show progress
    print("Processing:", filename)

    # Get some metadata from filename using league code definitions from helpers
    filename_data = filename[:-5].split("-")
    year = filename_data[1]


    # Create path for file and if file exists, open to read
    path = os.path.join(directory, filename)
    if os.path.isfile(path):
        with open(path, "r", encoding="utf-8") as fp:
            
            # Use HTML parsing with Beautiful Soup
            soup = BeautifulSoup(fp, 'html.parser')

            # Find relevant table, get first 20 rows
            table = soup.find_all("tbody")[1]
            rows = table.find_all("tr")[:20]

            # Loop through table rows
            for row in rows:
                # Get table columns
                columns = row.find_all("td")
                # Assign column data to variables
                rank = columns[0].getText()
                country = columns[2].find("img").get("title")
                points = columns[13].getText()
                print(year, country, rank, points)

                # Create list of data using above variables, write as row to CSV
                row = [year, country, rank, points]
                writer.writerow(row)

# Close csv
f.close()