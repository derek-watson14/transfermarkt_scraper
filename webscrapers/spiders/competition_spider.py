import scrapy
from pathlib import Path

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from helpers import land_ids, land_id_defs, comp_code_defs

class CompetitionsSpider(scrapy.Spider):
    name = "competitions"

    def start_requests(self):
        urls = []
        for comp in competition_defs.keys():
            for land_id in land_ids:
                url = f"https://www.transfermarkt.com/home/abschneiden/pokalwettbewerb/{comp}/plus/0?land_id={land_id}"
                urls.append(url)
    
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        land_id = response.url.split("=")[-1]
        comp_code = response.url.split("/")[-3]

        
        base_path = Path(__file__).parent
        file_path = (base_path / f"../competition-pages/competitions-{comp_code}-{land_id}.html").resolve()

        with open(file_path, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file at {file_path}')