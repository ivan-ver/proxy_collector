from scrapy_splash import SplashRequest

from proxy_collector_scrapy.items import ProxyItem
from proxy_collector_scrapy.providers.Provider import Provider
from proxy_collector_scrapy.utils.util import Util


class FoxtoolsRu(Provider):
    main_url = 'http://foxtools.ru'
    urls = ['http://foxtools.ru/Proxy']
    lua_script = Util.read_lua_script()
    protocols = {'HTTP': 1,
                 'HTTPS': 2}
    pages = None
    next_list_is_empty = True


    def get_requests(self):
        for url in self.urls:
            yield super().get_request(url)


    def get_proxies(self, response):
        table = response.xpath("//table[@id='theProxyList']/tbody/tr")
        for row in table:
            pi = ProxyItem()
            pi['host'] = row.xpath('td[2]/text()').get()
            pi['port'] = row.xpath('td[3]/text()').get()
            pi['_type'] = self.protocols[row.xpath('td[6]/text()').get().strip()]
            pi['ping'] = None
            yield pi

    def get_next(self, response):
        if not self.pages and self.next_list_is_empty:
            self.pages = response.xpath("//div[@class='pager'][1]/a/@href").extract()
            self.next_list_is_empty = False
        if len(self.pages) != 0:
            return self.get_request(self.main_url + self.pages.pop(0))
        else:
            self.next_list_is_empty = True
            return None


