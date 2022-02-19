import scrapy
from pathlib import Path

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tm_lists import leagues, seasons

class TransfersSpider(scrapy.Spider):
    name = "transfers"

    def start_requests(self):
        urls = []
        for league in leagues:
            for season in seasons:
                url = f"https://www.transfermarkt.com/laliga/transfers/wettbewerb/{league}/plus/?saison_id={season}&s_w=&leihe=0&intern=0"
                urls.append(url) 
    
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        season = response.url.split("/")[-1].split("&")[0][-4:]
        league = response.url.split("/")[-3]
        
        base_path = Path(__file__).parent
        file_path = (base_path / f"../transfer-pages/noloantransfers-{league}-{season}.html").resolve()

        with open(file_path, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {file_path}')