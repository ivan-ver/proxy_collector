from abc import abstractmethod
from scrapy_splash import SplashRequest
from proxy_collector_scrapy.utils.util import Util


class Provider:
    PATTERN = "([0-9]{1,3}[\.]){3}[0-9]{1,3}:[0-9]{2,}"
    protocols = {
        'http': 1,
        'https': 2,
        'socs4': 3,
        'socs': 4
    }
    lua_script = Util.read_lua_script()

    @abstractmethod
    def get_requests(self):
        pass

    @abstractmethod
    def get_proxies(self, response):
        pass

    @abstractmethod
    def get_next(self, response):
        pass

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
