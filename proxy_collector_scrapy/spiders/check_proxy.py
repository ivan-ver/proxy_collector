import scrapy
from scrapy import Request
from proxy_collector_scrapy.utils.data_base import Database
from proxy_collector_scrapy.items import ProxyItem
import re

class CheckProxySpider(scrapy.Spider):
    name = 'check_proxy'
    start_urls = ['https://api.myip.com']
    proxy_list = None
    types = {
        'http': 1,
        'https': 2
    }

    def __init__(self):
        with Database() as db:
            self.proxy_list = db.get_all_unchecked_proxy()

    def start_requests(self):
        for i in range(len(self.proxy_list)):
            yield Request(url=self.start_urls[0],
                          callback=self.parse,
                          dont_filter=True)

    def parse(self, response):
        response_proxy = re.findall("\\d+\.\d+\.\d+\.\d+", response.xpath("//text()").get())[0]
        using_proxy = response.meta['proxy']
        print(response.meta['proxy'])
        print(response_proxy)
        if response_proxy in using_proxy:
            pi = ProxyItem()
            pi['host'] = response_proxy
            pi['port'] = using_proxy.split(':')[-1]
            pi['_type'] = self.types[using_proxy.split('://')[0]]
            pi['ping'] = None
            yield pi

