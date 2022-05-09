import scrapy
from pathlib import Path

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from helpers import multitier_leagues, last_ten_seasons

class MultitierSpider(scrapy.Spider):
    name = "multitiers"

    def start_requests(self):
        urls = []
        for league in multitier_leagues:
            for season in last_ten_seasons:
                url = f"https://www.transfermarkt.us/premier-league/tabelle/wettbewerb/{league}?saison_id={season}"
                urls.append(url) 
                
    
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        season = response.url.split("=")[1]
        league = response.url.split("/")[-1].split("?")[0]

        
        base_path = Path(__file__).parent
        file_path = (base_path / f"../multitier-pages/multitier-{league}-{season}.html").resolve()

        with open(file_path, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file at {file_path}')