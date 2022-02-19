import os, csv, re
from bs4 import BeautifulSoup
from tm_lists import (
    league_code_defs,
    parse_filename,
    get_team_xfer_headers,
    new_team_xfer_summary,
    parse_fee,
)

# Open file to store data
f = open("../../csv-data/team_transfer_data.csv", "w", encoding="utf-8", newline='')
writer = csv.writer(f)

# Write data headers
column_headers = get_team_xfer_headers()
writer.writerow(column_headers)

# Set directory and loop through all files therein
directory = "./transfer-pages"

# Pages list
pages = os.listdir(directory)

testpg = pages[0]
print("Processing:", testpg)

# Get some metadata from filename using league code definitions from tm_lists
filename_data = parse_filename(testpg)
league_country = filename_data["country"]
filename_data_list = filename_data.values()

path = os.path.join(directory, testpg)
if os.path.isfile(path):
    with open(path, "r", encoding="utf-8") as fp:
        # Use HTML parsing with Beautiful Soup
        soup = BeautifulSoup(fp, 'html.parser')

        # Get all club name divs
        club_name_divs = soup.find_all("div", id=re.compile("^to-\d"))
        
        count = 0
        # Loop through all teams in given season
        for div in club_name_divs:
            # Create blank summary dict
            summary = new_team_xfer_summary()
  
            # Add club name for this team
            summary["club"] = div.text

            parent = div.parent
            tables = parent.find_all("tbody")

            domestic = None

            # Calculate summary values for all INCOMING transfers
            xfers_in = tables[0]
            in_cells = xfers_in.find_all("td")
            for index, cell in enumerate(in_cells):
                if index % 9 == 7:
                    flag = cell.find("img")
                    if flag:
                        in_from = cell.find("img").get("alt")
                        if in_from == league_country:
                            summary["domestic_signings"] += 1
                            domestic = True
                        else:
                            summary["international_signings"] += 1
                            domestic = False
                    else:
                        summary["other_signings"] += 1
                    summary["total_signings"] += 1

                
                if index % 9 == 8:
                    fee_str = cell.text
                    
                    if fee_str[0] == "€":
                        fee = parse_fee(fee_str)
                        if domestic:
                            summary["domestic_expenditure"] += fee
                        else:
                            summary["international_expenditure"] += fee
                        summary["total_expenditure"] += fee
                        domestic = None

                    if fee_str == "?" and summary["complete_data"] == True:
                        summary["complete_data"] = False   

            # Calculate summary values for all OUTGOING transfers                     
            xfers_out = tables[1]
            out_cells = xfers_out.find_all("td")
            for index, cell in enumerate(out_cells):
                if index % 9 == 7:
                    flag = cell.find("img")
                    if flag:
                        out_to = cell.find("img").get("alt")
                        if out_to == league_country:
                            summary["domestic_departures"] += 1
                            domestic = True
                        else:
                            summary["international_departures"] += 1
                            domestic = False
                    else:
                        summary["other_departures"] += 1
                    summary["total_departures"] += 1
                
                if index % 9 == 8:
                    fee_str = cell.text
                    
                    if fee_str[0] == "€":
                        fee = parse_fee(fee_str)
                        if domestic:
                            summary["domestic_income"] += fee
                        else:
                            summary["international_income"] += fee
                        summary["total_income"] += fee
                        domestic = None

                    if fee_str == "?" and summary["complete_data"] == True:
                        summary["complete_data"] = False   
            print(summary)

        # # Create list of data using above variables, write as row to CSV
        # row = [country, league, year, club_count, tot_departures, tot_income, tot_arrivals, tot_expenses]
        # writer.writerow(row)

# Close csv
f.close()