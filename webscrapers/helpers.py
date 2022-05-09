seasons = [2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]

leagues = ["GB1", "L1", "IT1", "ES1", "FR1", "PO1", "NL1"]

multitier_leagues = ["GB1", "GB2", "L1", "L2", "IT1", "IT2", "ES1", "ES2", "FR1", "FR2"]
last_ten_seasons = [2021, 2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012]

league_code_defs = {
    "GB1": {"league": "Premier League", "country": "England", "tier": 1, "size": 20}, 
    "GB2": {"league": "EFL Championship", "country": "England", "tier": 2, "size": 24}, 
    "L1": {"league": "Bundesliga", "country": "Germany", "tier": 1, "size": 18}, 
    "L2": {"league": "2. Bundesliga", "country": "Germany", "tier": 2, "size": 18}, 
    "IT1": {"league": "Serie A", "country": "Italy", "tier": 1, "size": 20}, 
    "IT2": {"league": "Serie B", "country": "Italy", "tier": 2, "size": 20}, 
    "ES1": {"league": "La Liga", "country": "Spain", "tier": 1, "size": 20}, 
    "ES2": {"league": "Segunda División", "country": "Spain", "tier": 2, "size": 22}, 
    "FR1": {"league": "Ligue 1", "country": "France", "tier": 1, "size": 20}, 
    "FR2": {"league": "Ligue 2", "country": "France", "tier": 2, "size": 20}, 
    "PO1": {"league": "Primeira Liga", "country": "Portugal", "tier": 1, "size": 18}, 
    "NL1": {"league": "Eredivisie", "country": "Netherlands", "tier": 1, "size": 18},
}

season_conversion = {
    2005: "2005/06",
    2006: "2006/07",
    2007: "2007/08",
    2008: "2008/09",
    2009: "2009/10",
    2010: "2010/11",
    2011: "2011/12",
    2012: "2012/13",
    2013: "2013/14",
    2014: "2014/15",
    2015: "2015/16",
    2016: "2016/17",
    2017: "2017/18",
    2018: "2018/19",
    2019: "2019/20",
    2020: "2020/21",
    2021: "2021/22",
}

land_ids = ["75", "40", "189", "136", "122", "157", "50"]

land_id_defs = {
    "75": league_code_defs["IT1"],
    "40": league_code_defs["L1"],
    "189": league_code_defs["GB1"],
    "136": league_code_defs["PO1"],
    "122": league_code_defs["NL1"],
    "157": league_code_defs["ES1"],
    "50": league_code_defs["FR1"],
}

comp_code_defs = {
    "CL": "Champions League",
    "EL": "Europa League",
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
    elif fee_str[-2:] == "bn":
        fee_str = fee_str.replace("bn", "")
        nums = fee_str.split(".")
        return int(nums[0] + nums[1] + "0000000")
    else:
        return int(fee_str)

def calc_summary_vals(table, summary, direction, league_country):
    summary_copy = summary.copy()
    if direction == "in":
        player_direction = "signings"
        money_direction = "expenditure"
    elif direction == "out":
        player_direction = "departures"
        money_direction = "income"

    domestic = None
    cells = table.find_all("td")
    for index, cell in enumerate(cells):
        if index % 9 == 7:
            flag = cell.find("img")
            if flag:
                in_from = cell.find("img").get("alt")
                if in_from == league_country:
                    summary_copy["domestic_" + player_direction] += 1
                    domestic = True
                else:
                    summary_copy["international_" + player_direction] += 1
                    domestic = False
            else:
                summary_copy["other_" + player_direction] += 1
            summary_copy["total_" + player_direction] += 1

        
        if index % 9 == 8:
            fee_str = cell.text

            if fee_str:
                if fee_str == "?":
                    summary_copy["complete_data"] = False 
                
                if fee_str[0] == "€":
                    fee = parse_fee(fee_str)
                    if domestic:
                        summary_copy["domestic_" + money_direction] += fee
                    else:
                        summary_copy["international_" + money_direction] += fee
                    summary_copy["total_" + money_direction] += fee
                    domestic = None
            else:
                summary_copy["complete_data"] = False

    
    return summary_copy