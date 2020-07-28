# -*- coding: utf-8 -*-
import scrapy
from proxy_collector_scrapy.providers.premProxy import PremProxy
from proxy_collector_scrapy.items import ProxyItem


class GetProxiesSpider(scrapy.Spider):
    name = 'get_proxies'
    __providers = [
        PremProxy(),
    ]

    def start_requests(self):
        for provider in self.__providers:
            for req in provider.get_requests():
                req.callback = self.main_parse
                yield req

    def main_parse(self, response, provider):
        yield provider.get_proxies(response)
        req = provider.get_next(response)
        if req:
            yield req

    def parse(self, response):
        pass

