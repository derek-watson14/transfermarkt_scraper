import scrapy
from tm_lists import seasons, leagues


class TransfersSpider(scrapy.Spider):
    name = "transfers"

    def start_requests(self):
        urls = []
        for league in leagues:
            for season in seasons:
                url = f"https://www.transfermarkt.com/laliga/transfers/wettbewerb/{league}/plus/?saison_id={season}"
                urls.append(url) 
    
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        season = response.url[-4:]
        league = response.url.split("/")[-3]
        filename = f'./transfer-pages/transfers-{league}-{season}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')