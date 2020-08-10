import re
from proxy_collector_scrapy.items import ProxyItem
from proxy_collector_scrapy.providers.Provider import Provider
from proxy_collector_scrapy.utils.util import Util


class ProxylistdailyNet(Provider):
    urls = ['https://www.proxylistdaily.net/']
    lua_script = Util.read_lua_script()

    def get_requests(self):
        for url in self.urls:
            yield super().get_request(url)

    def get_proxies(self, response):
        lists = response.xpath("//div[@class ='centeredProxyList freeProxyStyle']/span/span/text()").extract()
        for _list in lists:
            for row in _list.split('\n'):
                if re.match(super().PATTERN, row):
                    pi = ProxyItem()
                    pi['host'] = row.split(':')[0]
                    pi['port'] = row.split(':')[1]
                    pi['_type'] = 0
                    pi['ping'] = None
                    yield pi

    def get_next(self, response):
        return None
