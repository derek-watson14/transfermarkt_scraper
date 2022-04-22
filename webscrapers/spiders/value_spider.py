import scrapy
from pathlib import Path

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from helpers import leagues, seasons

class ValuesSpider(scrapy.Spider):
    name = "values"

    def start_requests(self):
        urls = []
        for league in leagues:
            for season in seasons:
                url = f"https://www.transfermarkt.us/premier-league/startseite/wettbewerb/{league}/plus/?saison_id={season}"
                urls.append(url) 
                
    
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        season = response.url.split("=")[1]
        league = response.url.split("/")[-3]
        print(response)

        
        base_path = Path(__file__).parent
        file_path = (base_path / f"../value-pages/values-{league}-{season}.html").resolve()

        with open(file_path, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file at {file_path}')