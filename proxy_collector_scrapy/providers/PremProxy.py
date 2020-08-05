import scrapy_splash
from scrapy_splash import SplashRequest

from proxy_collector_scrapy.items import ProxyItem
from proxy_collector_scrapy.providers.Provider import Provider
from proxy_collector_scrapy.utils.util import Util


class PremProxy(Provider):
    urls = ["http://premproxy.com/list/",
            "https://premproxy.com/socks-list"]

    types_ = {'SOCKS4': 4,
              'SOCKS5': 5,
              'elite': 1,
              'anonymous': 1
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
            return self.get_request(self.urls[0] + next_page)
        else:
            return None

    def get_proxies(self, response):
        proxies = list()
        for row in response.xpath("//table[@id='proxylistt']/tbody/tr")[:-1]:
            if row.xpath("td[2]/text()").get().strip() != 'transparent':
                pi = ProxyItem()
                pi['host'] = row.xpath("td[1]/text()").get()[:-1]
                pi['port'] = row.xpath("td[1]/span/text()").get()
                pi['_type'] = self.types_[row.xpath("td[2]/text()").get().strip()]
                pi['ping'] = None
                proxies.append(pi)
        return proxies
