from proxy_collector_scrapy.items import ProxyItem
from proxy_collector_scrapy.providers.Provider import Provider


class ProxypediaOrg(Provider):
    urls = ["https://proxypedia.org"]

    def get_requests(self):
        for url in self.urls:
            yield super().get_request(url)

    def get_proxies(self, response):
        _list = response.xpath('//ul/li/a/text()').extract()
        for row in _list:
            pi = ProxyItem()
            pi['host'] = row.split(':')[0]
            pi['port'] = row.split(':')[1]
            pi['_type'] = None
            pi['ping'] = None
            yield pi

    def get_next(self, response):
        return None