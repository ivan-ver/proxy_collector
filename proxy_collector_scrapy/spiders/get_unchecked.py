# -*- coding: utf-8 -*-
import scrapy

from proxy_collector_scrapy.providers.MyProxyCom import MyProxyCom
from proxy_collector_scrapy.providers.PremproxyCom import PremproxyCom
from proxy_collector_scrapy.providers.GetfreeproxylistsBlogspotCom import GetfreeproxylistsBlogspotCom
from proxy_collector_scrapy.providers.OnlineProxyRu import OnlineProxyRu
from proxy_collector_scrapy.providers.FreeProxyListNet import FreeProxyListNet
from proxy_collector_scrapy.providers.ProxypediaOrg import ProxypediaOrg
from proxy_collector_scrapy.providers.TwoIpRu import TwoIpRu
from proxy_collector_scrapy.providers.FoxtoolsRu import FoxtoolsRu
from proxy_collector_scrapy.providers.Ab57Ru import Ab57Ru
from proxy_collector_scrapy.providers.ProxytrueTk import ProxytrueTk
from proxy_collector_scrapy.providers.ProxylistdailyNet import ProxylistdailyNet
from proxy_collector_scrapy.providers.HideMyNameRu import HideMyNameRu
from proxy_collector_scrapy.providers.MultiproxyOrg import MultiproxyOrg
from proxy_collector_scrapy.providers.ApiProxyscrapeCom import ApiProxyscrapeCom
from proxy_collector_scrapy.providers.RootjazzComParse import RootjazzComParse
from proxy_collector_scrapy.providers.IpCn import IpCn



class GetProxiesSpider(scrapy.Spider):
    name = 'get_unchecked'

    custom_settings = {
        'DOWNLOAD_DELAY': 0,
        'DOWNLOAD_TIMEOUT': 10,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 20,
        'CONCURRENT_REQUESTS_PER_IP': 20,
        'CONCURRENT_REQUESTS': 20,
    }

    providers = [
        PremproxyCom(),
        MyProxyCom(),
        GetfreeproxylistsBlogspotCom(),
        OnlineProxyRu(),
        ProxypediaOrg(),
        FreeProxyListNet(),
        TwoIpRu(),
        FoxtoolsRu(),
        Ab57Ru(),
        ProxytrueTk(),
        ProxylistdailyNet(),
        HideMyNameRu(),
        MultiproxyOrg(),
        ApiProxyscrapeCom(),
        RootjazzComParse(),
        IpCn()
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
