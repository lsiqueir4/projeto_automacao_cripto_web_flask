#from urllib.request import Request
import scrapy
import time
from scrapy.crawler import CrawlerProcess

links = ['bombcrypto',
        'cryptocars',
        'cryptomotorcycle',
        'smooth-love-potion',
        'cryptoguards',
        'bitcoin'
        ]

class CriptoflaskSpider(scrapy.Spider):
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES' : {
                'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
                'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
            }, 'DOWNLOAD_DELAY' : 1
    }
    
    name = 'criptoflask_spider'
    start_urls = [f'https://coinmarketcap.com/pt-br/currencies/{i}/' for i in links]
    
    
    def parse(self, response):
        yield {
            'nome' : response.css('.h1 ::text').get(),
            'sigla' : response.css('.nameSymbol ::text').get(),
            'cotacao' : response.css('.priceValue span ::text').get()
            }
        time.sleep(2)

#para chamar o crawler pelo script
# def chamar_spider():
#         process = CrawlerProcess()
#         process.crawl(CriptoflaskSpider)
#         process.start()
        

