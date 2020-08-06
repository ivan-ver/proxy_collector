from proxy_collector_scrapy.items import ProxyItem
from proxy_collector_scrapy.providers.Provider import Provider
from proxy_collector_scrapy.utils.util import Util


class OnlineProxyRu(Provider):
    urls = ['http://online-proxy.ru']
    lua_script = Util.read_lua_script()
    types = {
        'HTTP': 2,
        'HTTPS': 3,
        'HTTP/HTTPS': 3
    }

    def get_requests(self):
        for url in self.urls:
            yield super().get_request(url)

    def get_proxies(self, response):
        table = response.xpath("//td[@class='content']/table[1]/tbody/tr")[1:]
        for row in table:
            if row.xpath('td/text()').extract()[4] != 'прозрачный':
                pi = ProxyItem()
                pi['host'] = row.xpath('td[2]/text()').get()
                pi['port'] = row.xpath('td[3]/text()').get()
                pi['_type'] = self.types[row.xpath('td[4]/text()').get()]
                pi['ping'] = int(row.xpath('td[10]/text()').get())
                yield pi

    def get_next(self, response):
        return None
