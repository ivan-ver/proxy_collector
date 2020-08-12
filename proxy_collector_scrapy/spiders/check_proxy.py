import scrapy
from scrapy import Request
from proxy_collector_scrapy.utils.data_base import Database
from proxy_collector_scrapy.items import ProxyItem


class CheckProxySpider(scrapy.Spider):
    name = 'check_proxy'
    start_urls = ['http://ipinfo.io/ip/']
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
        responsing_url = response.xpath("//text()").get()
        using_proxy = response.meta['proxy']
        print(response.meta['proxy'])
        print(response.xpath("//text()").get())
        if responsing_url in using_proxy:
            pi = ProxyItem()
            pi['host'] = responsing_url
            pi['port'] = using_proxy.split(':')[-1]
            pi['_type'] = self.types[using_proxy.split('://')[0]]
            pi['ping'] = None
            yield pi

