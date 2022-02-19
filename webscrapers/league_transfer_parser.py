import os
import csv
from bs4 import BeautifulSoup
from helpers import league_code_defs

# Open file to store data
f = open("../../csv-data/league_transfer_data.csv", "w", encoding="utf-8", newline='')
writer = csv.writer(f)

# Write data headers
column_headers = ["Country", "League", "Year", "Club Count", "Total Departures", "Total Income", "Total Arrivals", "Total Expenses"]
writer.writerow(column_headers)

# Set directory and loop through all files therein
directory = "./transfer-pages"

# Change euro string into int
def euros2int(val):
    digit_groups = val[1:].split(",")
    number = ""
    for group in digit_groups:
        number += group
    return int(number)
    

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

            # Get number of clubs based on count of a tag
            club_count = int(len(soup.find_all("div", class_= "transfer-zusatzinfo-box")) / 2)

            # Find section with summary numbers, and get lists of the relevant sections
            summary_data = soup.find("div", class_= "transferbilanz")
            headers = summary_data("b")
            numbers = summary_data("span")

            # Assign correct summary data values to variables
            tot_departures = int(headers[0].text)
            tot_arrivals = int(headers[1].text)
            tot_income = euros2int(numbers[0].text)
            tot_expenses = euros2int(numbers[3].text)

            # Create list of data using above variables, write as row to CSV
            row = [country, league, year, club_count, tot_departures, tot_income, tot_arrivals, tot_expenses]
            writer.writerow(row)

# Close csv
f.close()