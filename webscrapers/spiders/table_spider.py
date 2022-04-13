import scrapy
from pathlib import Path

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from helpers import leagues, seasons

class TablesSpider(scrapy.Spider):
    name = "tables"

    def start_requests(self):
        urls = []
        for league in leagues:
            for season in seasons:
                url = f"https://www.transfermarkt.us/premier-league/tabelle/wettbewerb/{league}?saison_id={season}"
                urls.append(url) 
                
    
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        season = response.url.split("=")[1]
        league = response.url.split("/")[-1].split("?")[0]

        
        base_path = Path(__file__).parent
        file_path = (base_path / f"../table-pages/tables-{league}-{season}.html").resolve()

        with open(file_path, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file at {file_path}')