seasons = [2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]

leagues = ["GB1", "L1", "IT1", "ES1", "FR1", "PO1", "NL1"]

league_code_defs = {
    "GB1": {"league": "Premier League", "country": "England"}, 
    "L1": {"league": "Bundesliga", "country": "Germany"}, 
    "IT1": {"league": "Serie A", "country": "Italy"}, 
    "ES1": {"league": "La Liga", "country": "Spain"}, 
    "FR1": {"league": "Ligue 1", "country": "France"}, 
    "PO1": {"league": "Primeira Liga", "country": "Portugal"}, 
    "NL1": {"league": "Eredivisie", "country": "Netherlands"},
}

def parse_filename(filename):
    filename_data = filename[:-5].split("-")
    year = filename_data[2]
    league_code = filename_data[1]
    country = league_code_defs[league_code]["country"]
    league = league_code_defs[league_code]["league"]
    return {
        "country": country,
        "league": league,
        "year": year,
    }

def new_team_xfer_summary():
    return {
        "club": None,
        "domestic_expenditure": 0,
        "international_expenditure": 0,
        "total_expenditure": 0,
        "domestic_income": 0,
        "international_income": 0,
        "total_income": 0,
        "domestic_signings": 0,
        "international_signings": 0,
        "other_signings": 0,
        "total_signings": 0,
        "domestic_departures": 0,
        "international_departures": 0,
        "other_departures": 0,
        "total_departures": 0,
        "complete_data": True,
    }

def get_team_xfer_headers():
    general_headers = ["country", "league", "year"]
    xfer_headers = list(new_team_xfer_summary().keys())
    return general_headers + xfer_headers

def parse_fee(fee_str):
    fee_str = fee_str.replace("€", "")
    if fee_str[-1] == "m":
        fee_str = fee_str.replace("m", "")
        nums = fee_str.split(".")
        return int(nums[0] + nums[1] + "0000")
    elif fee_str[-3:] == "Th.":
        fee_str = fee_str.replace("Th.", "")
        return int(fee_str + "000")