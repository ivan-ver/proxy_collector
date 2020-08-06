from scrapy_splash import SplashRequest

from proxy_collector_scrapy.items import ProxyItem
from proxy_collector_scrapy.providers.Provider import Provider
from proxy_collector_scrapy.utils.util import Util


class MyProxyCom(Provider):
    main_page = 'https://www.my-proxy.com/'
    urls = ['https://www.my-proxy.com/free-elite-proxy.html',
            'https://www.my-proxy.com/free-anonymous-proxy.html',
            'https://www.my-proxy.com/free-transparent-proxy.html',
            'https://www.my-proxy.com/free-socks-4-proxy.html',
            'https://www.my-proxy.com/free-socks-5-proxy.html',
            'https://www.my-proxy.com/free-proxy-list.html',
            'https://www.my-proxy.com/free-proxy-list-2.html',
            'https://www.my-proxy.com/free-proxy-list-3.html',
            'https://www.my-proxy.com/free-proxy-list-4.html',
            'https://www.my-proxy.com/free-proxy-list-5.html',
            'https://www.my-proxy.com/free-proxy-list-6.html',
            'https://www.my-proxy.com/free-proxy-list-7.html',
            'https://www.my-proxy.com/free-proxy-list-8.html',
            'https://www.my-proxy.com/free-proxy-list-9.html',
            'https://www.my-proxy.com/free-proxy-list-10.html'
            ]
    lua_script = Util.read_lua_script()

    def get_requests(self):
        for url in self.urls:
            yield self.get_request(url)

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

    def get_proxies(self, response):
        result = []
        current_type = None
        if 'socks-5' in response.url:
            current_type = 5
        elif 'socks-4' in response.url:
            current_type = 4
        else:
            current_type = 1
        for p in response.xpath("//div[@class='list']/text()").extract():
            pi = ProxyItem()
            v = (p.split('#')[0]).split(':')
            pi['host'] = v[0]
            pi['port'] = v[1]
            pi['_type'] = current_type
            pi['ping'] = None
            result.append(pi)
            # yield pi
        return result

    def get_next(self, response):
        return None