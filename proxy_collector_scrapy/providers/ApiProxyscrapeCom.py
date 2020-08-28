import re
from proxy_collector_scrapy.items import ProxyItem
from proxy_collector_scrapy.providers.Provider import Provider
from proxy_collector_scrapy.utils.util import Util


class ApiProxyscrapeCom(Provider):
    urls = [
        'https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=all&ssl=yes&anonymity=elite',
        'https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=all&ssl=no&anonymity=elite',
        'https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=all&ssl=yes&anonymity=anonymous',
        'https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=all&ssl=no&anonymity=anonymous',
        'https://api.proxyscrape.com/?request=getproxies&proxytype=socks4&timeout=10000&country=all&ssl=yes&anonymity=anonymous',
        'https://api.proxyscrape.com/?request=getproxies&proxytype=socks5&timeout=10000&country=all&ssl=yes&anonymity=anonymous'
    ]
    lua_script = Util.read_lua_script()

    def get_requests(self):
        for url in self.urls:
            yield super().get_request(url)

    def get_proxies(self, response):
        proxy_list = response.text.split('\n')
        for row in proxy_list:
            pi = ProxyItem()
            pi['host'] = row.split(':')[0]
            pi['port'] = row.split(':')[1].strip()
            pi['_type'] = 0
            pi['ping'] = None
            yield pi


    def get_next(self, response):
        return None
