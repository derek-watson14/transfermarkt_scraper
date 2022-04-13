import scrapy
from pathlib import Path

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from helpers import land_ids, land_id_defs, competition_defs

class StadiumsSpider(scrapy.Spider):
    name = "competitions"

    def start_requests(self):
        competitions = ["CL", "EL"]
        urls = []
        for comp in competitions:
            for land_id in land_ids:
                url = f"https://www.transfermarkt.us/home/abschneiden/pokalwettbewerb/{comp}/plus/0?land_id={land_id}"
                urls.append(url) 
                
    
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        land_id = response.url.split("=")[-1]
        comp_code = response.url.split("/")[-3]

        country = land_id_defs[land_id]["country"]
        competition = f"{competition_defs[comp_code].split()[0]}_{competition_defs[comp_code].split()[1]}"

        
        base_path = Path(__file__).parent
        file_path = (base_path / f"../competition-pages/competitions-{competition}-{country}.html").resolve()

        with open(file_path, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file at {file_path}')