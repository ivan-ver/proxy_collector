import scrapy
from scrapy import Request
from proxy_collector_scrapy.utils.data_base import Database
from proxy_collector_scrapy.items import ProxyItem
import re

class CheckProxySpider(scrapy.Spider):
    name = 'check_proxy'

    custom_settings = {
        'DOWNLOAD_DELAY': 0,
        'DOWNLOAD_TIMEOUT': 30,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 200,
        'CONCURRENT_REQUESTS_PER_IP': 200,
        'CONCURRENT_REQUESTS': 400,
    }

    start_urls = ['https://www.google.ru']
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
        # response_proxy = 'abc'
        # try:
        #     response_proxy = re.findall("\\d+\.\d+\.\d+\.\d+", response.xpath("//text()").get())[0]
        # except:
        #     pass
        # using_proxy = response.meta['proxy']
        if response.status == 200:
            using_proxy = response.meta['proxy']
            pi = ProxyItem()
            pi['host'] = (using_proxy.split('://')[-1]).split(':')[0]
            pi['port'] = using_proxy.split(':')[-1]
            pi['_type'] = self.types[using_proxy.split('://')[0]]
            pi['ping'] = None
            yield pi

