import scrapy
from scrapy import Request
from proxy_collector_scrapy.utils.data_base import Database


class CheckProxySpider(scrapy.Spider):
    name = 'check_proxy'
    start_urls = 'http://ipinfo.io/ip/'
    proxy_list = None

    def __init__(self):
        with Database() as db:
            self.proxy_list = db.get_all_unchecked_proxy()

    def start_requests(self):
        for proxy in self.proxy_list:
            if proxy['type'] != 4:
                pf = 'https://' + proxy['host']+':'+str(proxy['port'])
                print(pf)
                yield Request(url=self.start_urls, meta={'proxy': pf})

    def parse(self, response):
        current_url = response.xpath("//body/text()")
        print("123" + current_url)