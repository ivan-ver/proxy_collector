from proxy_collector_scrapy.providers.Provider import Provider
from proxy_collector_scrapy.items import ProxyItem


class ProxytrueTk(Provider):
    urls = ['http://proxytrue.tk/']

    def get_requests(self):
        for url in self.urls:
            yield super().get_request(url)

    def get_proxies(self, response):
        table = response.xpath("//table[@class ='table table-striped']//tr/td[1]/text()").extract()
        for string in table:
            pi =ProxyItem()
            pi['host'] = string.split(':')[0]
            pi['port'] = string.split(':')[1]
            pi['_type'] = 0
            pi['ping'] = None
            yield pi

    def get_next(self, response):
        return None
