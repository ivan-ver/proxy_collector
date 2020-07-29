import scrapy_splash
from scrapy_splash import SplashRequest

from proxy_collector_scrapy.items import ProxyItem
from proxy_collector_scrapy.providers.Provider import Provider
from proxy_collector_scrapy.utils.util import Util


class PremProxy(Provider):
    urls = ["http://premproxy.com/list/",
            "https://premproxy.com/socks-list"]

    types_ = {'SOCKS4 ': 4,
              'SOCKS5 ': 5,
              'elite ': 1,
              'anonymous ': 1
              }

    lua_script = Util.read_lua_script()

    def get_requests(self):
        return [self.get_request(url) for url in self.urls]

    def get_request(self, url):
        return SplashRequest(
            url=url,
            endpoint='execute',
            cache_args=['lua_source'],
            args={
                'lua_source': self.lua_script
            },
            cb_kwargs={'provider': self}
        )

    def get_next(self, response):
        next_page = response.xpath("//div[@id='navbar'][1]//li/a[text()='next']/@href").get()
        if next_page:
            return self.get_request(response.follow(next_page).url)

    def get_proxies(self, response):
        ips = response.xpath("//table[@id='proxylistt']//tr/td[1]/text()").extract()[:-1]
        ports = response.xpath("//table[@id='proxylistt']//tr/td[1]/span/text()").extract()
        types = response.xpath("//table[@id='proxylistt']//tr/td[2]/text()").extract()

        proxies = list()
        for i in range(len(ips)):
            pi = ProxyItem()
            if types[i] != 'transparent ':
                pi['host'] = ips[i][:-1]
                pi['port'] = int(ports[i])
                pi['_type'] = self.types_[types[i]]
                pi['ping'] = None
                proxies.append(pi)

        return proxies
