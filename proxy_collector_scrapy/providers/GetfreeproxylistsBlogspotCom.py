from scrapy_splash import SplashRequest

from proxy_collector_scrapy.items import ProxyItem
from proxy_collector_scrapy.providers.Provider import Provider
from proxy_collector_scrapy.utils.util import Util


class GetfreeproxylistsBlogspotCom(Provider):
    urls = ['https://getfreeproxylists.blogspot.com/']
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
        res = list()
        blocks = [response.xpath("//div[@id='post-body-8210650074430112200']"),
            response.xpath("//div[@id='post-body-1883764469148519908']"),
            response.xpath("//div[@id='post-body-4499055043126441170']"),
            response.xpath("//div[@id='post-body-5129256980014740999']"),
            response.xpath("//div[@id='post-body-227127606125474560']"),
            response.xpath("//div[@id='post-body-4685080276688808120']"),
            response.xpath("//div[@id='post-body-8318323332517554290']")]

        for block in blocks:
            r = block.xpath("text()").extract()
            print()

        pass

    def get_next(self, response):
        pass
