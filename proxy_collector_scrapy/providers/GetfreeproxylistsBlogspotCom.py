import re
from proxy_collector_scrapy.items import ProxyItem
from proxy_collector_scrapy.providers.Provider import Provider
from proxy_collector_scrapy.utils.util import Util

PATTERN = "([0-9]{1,3}[\.]){3}[0-9]{1,3}:[0-9]{2,}"

class GetfreeproxylistsBlogspotCom(Provider):
    urls = ['https://getfreeproxylists.blogspot.com']
    lua_script = Util.read_lua_script()

    def get_requests(self):
        for url in self.urls:
            yield super().get_request(url)

    def get_proxies(self, response):
        blocks = [response.xpath("//div[@id='post-body-8210650074430112200']"),
            response.xpath("//div[@id='post-body-1883764469148519908']"),
            response.xpath("//div[@id='post-body-4499055043126441170']"),
            response.xpath("//div[@id='post-body-5129256980014740999']"),
            response.xpath("//div[@id='post-body-227127606125474560']"),
            response.xpath("//div[@id='post-body-4685080276688808120']"),
            response.xpath("//div[@id='post-body-8318323332517554290']")]

        for block in blocks:
            block_content = block.xpath("descendant-or-self::*/text()").extract()
            current_type = None
            for content in block_content:
                if content == 'HTTP':
                    current_type = 1
                elif content == 'HTTPS':
                    current_type = 2
                elif re.match(PATTERN, content):
                    pi = ProxyItem()
                    pi['host'] = content.split(':')[0]
                    pi['port'] = content.split(':')[1]
                    pi['_type'] = current_type
                    pi['ping'] = None
                    yield pi

    def get_next(self, response):
        pass
