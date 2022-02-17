import scrapy


class StadiumsSpider(scrapy.Spider):
    name = "stadiums"

    def start_requests(self):
        seasons = [2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]
        leagues = ["GB1", "L1", "IT1", "ES1", "FR1", "PO1", "NL1"]
        urls = []
        for league in leagues:
            for season in seasons:
                url = f"https://www.transfermarkt.us/laliga/besucherzahlen/wettbewerb/{league}/plus/1?saison_id={season}"
                urls.append(url) 
    
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        season = response.url[-4:]
        league = response.url.split("/")[-3]
        filename = f'./stadium-pages/stadium-{league}-{season}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')