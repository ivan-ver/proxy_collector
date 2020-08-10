from scrapy_splash import SplashRequest
import re
from proxy_collector_scrapy.items import ProxyItem
from proxy_collector_scrapy.providers.Provider import Provider
from proxy_collector_scrapy.utils.util import Util


class Ab57Ru(Provider):
    urls = ['https://ab57.ru/proxylist.html']
    lua_script = Util.read_lua_script()

    def get_requests(self):
        for url in self.urls:
            yield super().get_request(url)

    def get_proxies(self, response):
        _list = response.xpath('//table/tr/td[2]/pre/text()').extract()
        for row in _list:
            for string in row.split('\r\n'):
                if re.match(super().PATTERN, string):
                    pi = ProxyItem()
                    pi['host'] = string.split(':')[0]
                    pi['port'] = string.split(':')[1]
                    pi['_type'] = 0
                    pi['ping'] = None
                    yield pi

    def get_next(self, response):
        return None
