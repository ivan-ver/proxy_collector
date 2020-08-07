from scrapy import Request
from proxy_collector_scrapy.items import ProxyItem
from proxy_collector_scrapy.providers.Provider import Provider


class FreeProxyListNet(Provider):
    urls = ["https://free-proxy-list.net",
            "https://free-proxy-list.net/uk-proxy.html",
            "https://www.sslproxies.org",
            "https://free-proxy-list.net/anonymous-proxy.html",
            ]

    def get_requests(self):
        for url in self.urls:
            yield self.get_request(url)

    def get_request(self, url):
        return Request(
            url=url,
            cb_kwargs={'provider': self}
        )

    def get_proxies(self, response):
        table = response.xpath("//table[@id='proxylisttable']/tbody/tr")
        for row in table:
            pi = ProxyItem()
            pi['host'] = row.xpath('td[1]/text()').get()
            pi['port'] = row.xpath('td[2]/text()').get()
            if row.xpath('td[7]/text()').get() == 'no':
                pi['_type'] = 1
            else:
                pi['_type'] = 2
            pi['ping'] = None
            yield pi

    def get_next(self, response):
        return None
