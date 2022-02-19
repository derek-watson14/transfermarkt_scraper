import os, csv, re
from bs4 import BeautifulSoup
from helpers import (
    league_code_defs,
    parse_filename,
    get_team_xfer_headers,
    new_team_xfer_summary,
    parse_fee,
    calc_summary_vals,
)

# Open file to store data
f = open("../../csv-data/team_transfer_data.csv", "w", encoding="utf-8", newline='')
writer = csv.writer(f)

# Write data headers
column_headers = get_team_xfer_headers()
writer.writerow(column_headers)

# Set directory and loop through all files therein
directory = "./transfer-pages"

for filename in os.listdir(directory):
    print("Processing:", filename)

    # Get some metadata from filename using league code definitions from helpers
    filename_data = parse_filename(filename)

    path = os.path.join(directory, filename)
    if os.path.isfile(path):
        with open(path, "r", encoding="utf-8") as fp:
            # Use HTML parsing with Beautiful Soup
            soup = BeautifulSoup(fp, 'html.parser')

            # Get all club name divs
            club_name_divs = soup.find_all("div", id=re.compile("^to-\d"))
            
            # Loop through all teams in given season
            for div in club_name_divs:
                # Create blank summary dict
                summary = new_team_xfer_summary()
    
                # Add club name for this team
                summary["club"] = div.text

                parent = div.parent
                tables = parent.find_all("tbody")
                summary = calc_summary_vals(tables[0], summary, "in", filename_data["country"])
                summary = calc_summary_vals(tables[1], summary, "out", filename_data["country"])
                
                row = list(filename_data.values()) + list(summary.values())
                writer.writerow(row)

# Close csv
f.close()