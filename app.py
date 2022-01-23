from flask import Flask, render_template, request
import os, time, scrapy
from scrapy.crawler import CrawlerProcess

app = Flask(__name__)


cripto_lista = []

#home
@app.route('/', methods = ['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('home.html')
    #pegando os dados do checkbox como list
    if request.method == 'POST':
        data = request.form.getlist('criptomoedas')
        for i in data:
            cripto_lista.append(i) 
        print(cripto_lista)
        chamar_spider()
        return render_template('home.html')

#spider do Scrapy para coleta das cotacoes
class CriptoflaskSpider(scrapy.Spider):
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES' : {
                'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
                'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
            }, 'DOWNLOD_DELAY': 1
        
    }
    
    name = 'criptoflask_spider'
    start_urls = [f'https://coinmarketcap.com/pt-br/currencies/{i}/' for i in cripto_lista]
    
    
    def parse(self, response):
        yield {
            'nome' : response.css('.h1 ::text').get(),
            'sigla' : response.css('.nameSymbol ::text').get(),
            'cotacao' : response.css('.priceValue span ::text').get()
            }
        time.sleep(2)

#para chamar o crawler pelo script
def chamar_spider():
    process.crawl(CriptoflaskSpider)
    process.start()

if __name__ == '__main__':
    process = CrawlerProcess()
    #rodando o web
    app.run(debug=True)