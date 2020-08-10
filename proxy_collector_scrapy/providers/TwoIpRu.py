from scrapy_splash import SplashRequest

from proxy_collector_scrapy.items import ProxyItem
from proxy_collector_scrapy.providers.Provider import Provider
from proxy_collector_scrapy.utils.util import Util


class TwoIpRu(Provider):
    urls = ['https://2ip.ru/proxy/']
    lua_script = Util.read_lua_script()

    def get_requests(self):
        for url in self.urls:
            yield super().get_request(url)


    def get_proxies(self, response):
        table = response.xpath("//div[@id='content']//table//tr/td[1]/text()").extract()
        for proxy in table:
            current_proxy = proxy.strip()
            pi = ProxyItem()
            pi['host'] = current_proxy.split(':')[0]
            pi['port'] = current_proxy.split(':')[1]
            pi['_type'] = 0
            pi['ping'] = None
            yield pi

    def get_next(self, response):
        return None
