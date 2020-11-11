import re
from proxy_collector_scrapy.items import ProxyItem
from proxy_collector_scrapy.providers.Provider import Provider
from proxy_collector_scrapy.utils.util import Util



class GetfreeproxylistsBlogspotCom(Provider):
    urls = ['https://getfreeproxylists.blogspot.com']
    lua_script = Util.read_lua_script()

    def get_requests(self):
        for url in self.urls:
            yield super().get_request(url)

    def get_proxies(self, response):
        blocks = response.xpath("//div[@class='post-body entry-content']")
        for block in blocks:
            block_content = block.xpath("descendant-or-self::*/text()").extract()
            current_type = None
            for content in block_content:
                if content == 'HTTP':
                    current_type = 1
                elif content == 'HTTPS':
                    current_type = 2
                elif re.match(super().PATTERN, content):
                    pi = ProxyItem()
                    pi['host'] = content.split(':')[0]
                    pi['port'] = content.split(':')[1]
                    pi['_type'] = current_type
                    pi['ping'] = None
                    yield pi

    def get_next(self, response):
        pass
