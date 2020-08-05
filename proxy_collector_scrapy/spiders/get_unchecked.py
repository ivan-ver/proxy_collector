# -*- coding: utf-8 -*-
import scrapy
from proxy_collector_scrapy.providers.PremproxyCom import PremproxyCom
from proxy_collector_scrapy.providers.MyProxyCom import MyProxyCom
from proxy_collector_scrapy.items import ProxyItem


class GetProxiesSpider(scrapy.Spider):
    name = 'get_unchecked'
    providers = [
        PremproxyCom(),
        MyProxyCom()
    ]

    def start_requests(self):
        for provider in self.providers:
            for req in provider.get_requests():
                req.callback = self.main_parse
                yield req

    def main_parse(self, response, provider):
        for item in provider.get_proxies(response):
            yield item
        req = provider.get_next(response)
        if req:
            req.callback = self.main_parse
            yield req

    def parse(self, response):
        pass
