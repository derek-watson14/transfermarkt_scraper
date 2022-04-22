import os
import csv
from bs4 import BeautifulSoup

# Open file to store data
f = open("../../csv-data/combined.csv", "w", encoding="utf-8", newline='')
writer = csv.writer(f)

# Write data headers
column_headers = [
    "ID",
    "Country", 
    "League", 
    "Year", 
    "Club",
    "Stadium",
    "Stadium Capacity",
    "Season Total Spectators",
    "Season Average Spectators",
    "Total Matches",
    "Average Attendance Percentage",
    "Table Position", 
    "Points", 
    "Goal Differential",
    "Squad Size",
    "Average Age",
    "Foreigners in Squad",
    "Market Value Per Player",
    "Total Market Value",
    "Domestic Expenditure",
    "International Expenditure",
    "Total Expenditure",
    "Domestic Income",
    "International Income",
    "Total Income",
    "Domestic Signings",
    "International Signings",
    "Other Signings",
    "Total Signings",
    "Domestic Departures",
    "International Departures",
    "Other Departures",
    "Total Departures",
    "Complete Transfer Data?"
]
writer.writerow(column_headers)

# Open Stadium CSV
stadiums = open("../../csv-data/stadium_data.csv", "r", encoding="utf-8", newline='')
stadium_reader = csv.reader(stadiums)
next(stadium_reader)

# Open Table CSV
tables = open("../../csv-data/league_table_data.csv", "r", encoding="utf-8", newline='')
table_reader = csv.reader(tables)
next(table_reader)

# Open Value CSV
values = open("../../csv-data/squad_value_data.csv", "r", encoding="utf-8", newline='')
value_reader = csv.reader(values)
next(value_reader)

# Open Transfer CSV
transfers = open("../../csv-data/team_transfer_data.csv", "r", encoding="utf-8", newline='')
transfer_reader = csv.reader(transfers)
next(transfer_reader)

items = {}

for row in stadium_reader:
    row_id = f"{row[1]}{row[2]}{row[4]}".replace(" ", "")
    country = row[0]
    league = row[1]
    year = row[2]
    club = row[4]
    stadium = row[3]
    stadium_capacity = row[5]
    season_total_spectators = row[6]
    season_average_spectators = row[7]
    total_matches = row[8]
    average_attendance_percentage = row[10]
    items[row_id] = [
        row_id, 
        country, 
        league, 
        year, 
        club, 
        stadium, 
        stadium_capacity,
        season_total_spectators,
        season_average_spectators,
        total_matches,
        average_attendance_percentage
    ]

for row in table_reader:
    row_id = f"{row[1]}{row[2]}{row[4]}".replace(" ", "")
    table_position = row[3]
    points = row[5]
    goal_differential = row[6]
    new_data = [table_position, points, goal_differential]
    items[row_id] += new_data

for row in value_reader:
    row_id = f"{row[1]}{row[2]}{row[3]}".replace(" ", "")
    squad_size = row[4]
    average_age = row[5]
    foreigners = row[6]
    avg_market_value = row[7]
    tot_market_value = row[8]
    new_data = [squad_size, average_age, foreigners, avg_market_value, tot_market_value]
    items[row_id] += new_data

for row in transfer_reader:
    row_id = f"{row[1]}{row[2]}{row[3]}".replace(" ", "")
    domestic_expenditure = row[4]
    international_expenditure = row[5]
    total_expenditure = row[6]
    domestic_income = row[7]
    international_income = row[8]
    total_income = row[9]
    domestic_signings = row[10]
    international_signings = row[11]
    other_signings = row[12]
    total_signings = row[13]
    domestic_departures = row[14]
    international_departures = row[15]
    other_departures = row[16]
    total_departures = row[17]
    complete_data = row[18]
    new_data = [
        domestic_expenditure, 
        international_expenditure, 
        total_expenditure, 
        domestic_income, 
        international_income, 
        total_income, 
        domestic_signings, 
        international_signings, 
        other_signings, 
        total_signings, 
        domestic_departures, 
        international_departures, 
        other_departures, 
        total_departures, 
        complete_data
    ]
    items[row_id] += new_data

for row in items.values():
    writer.writerow(row)