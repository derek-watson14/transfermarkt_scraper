import scrapy
from pathlib import Path

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from helpers import seasons

class CoefficientSpider(scrapy.Spider):
    name = "coefficients"

    def start_requests(self):
        urls = []
        for season in seasons:
            url = f"https://www.transfermarkt.us/uefa/5jahreswertung/statistik/stat/saison_id/{season}/plus/1"
            urls.append(url) 
                
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        season = response.url.split("/")[-3]

        
        base_path = Path(__file__).parent
        file_path = (base_path / f"../coefficient-pages/coefficients-{season}.html").resolve()

        with open(file_path, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file at {file_path}')