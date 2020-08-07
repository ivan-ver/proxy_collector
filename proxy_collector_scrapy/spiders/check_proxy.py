import scrapy
from scrapy import Request
from proxy_collector_scrapy.utils.data_base import Database
from proxy_collector_scrapy.items import ProxyItem


class CheckProxySpider(scrapy.Spider):
    name = 'check_proxy'
    start_urls = 'http://ipinfo.io/ip'
    proxy_list = None
    types = {
        1: 'http://',
        2: 'https://'
    }

    def __init__(self):
        with Database() as db:
            self.proxy_list = db.get_all_unchecked_proxy()

    def start_requests(self):
        for i in range(len(self.proxy_list)):
            yield Request(url=self.start_urls,
                          callback=self.check_parse,
                          dont_filter=True)

    def check_parse(self, response, proxy, type):
        current_url = response.xpath("//text()").get()
        print("Correct " + self.types[type] + current_url)
        if current_url == proxy['host']:
            pi = ProxyItem()
            pi['host'] = proxy['host']
            pi['port'] = proxy['port']
            pi['_type'] = type
            pi['ping'] = None
            yield pi

