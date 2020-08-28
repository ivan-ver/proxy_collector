import re
from proxy_collector_scrapy.items import ProxyItem
from proxy_collector_scrapy.providers.Provider import Provider
from proxy_collector_scrapy.utils.util import Util


class MultiproxyOrg(Provider):
    urls = ['https://multiproxy.org/txt_anon/proxy.txt']
    lua_script = Util.read_lua_script()

    def get_requests(self):
        for url in self.urls:
            yield super().get_request(url)

    def get_proxies(self, response):
        proxy_list = response.text.split('\n')
        for row in proxy_list:
            if re.match(super().PATTERN, row):
                pi = ProxyItem()
                pi['host'] = row.split(':')[0]
                pi['port'] = row.split(':')[1]
                pi['_type'] = 0
                pi['ping'] = None
                yield pi


    def get_next(self, response):
        return None
