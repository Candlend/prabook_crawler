import scrapy

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "https://prabook.com/web/home.html",
    ]

    def parse(self, response):
        print(response.body)
