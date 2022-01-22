#from urllib.request import Request
import scrapy
import time

links = ['bombcrypto',
        'cryptocars',
        'cryptomotorcycle',
        'smooth-love-potion',
        'cryptoguards',
        'bitcoin'
        ]

class CriptoflaskSpiderSpider(scrapy.Spider):
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES' : {
                'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
                'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
            }
    }
    
    name = 'criptoflask_spider'
    start_urls = [f'https://coinmarketcap.com/pt-br/currencies/{i}/' for i in links ]
    
    
    def parse(self, response):
        yield {
            'nome' : response.css('.h1 ::text').get(),
            'sigla' : response.css('.nameSymbol ::text').get(),
            'cotacao' : response.css('.priceValue span ::text').get()
            }
        