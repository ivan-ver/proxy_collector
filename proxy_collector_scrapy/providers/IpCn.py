import re
from proxy_collector_scrapy.items import ProxyItem
from proxy_collector_scrapy.providers.Provider import Provider
from proxy_collector_scrapy.utils.util import Util


class IpCn(Provider):
    urls = [
        'https://www.89ip.cn/tqdl.html?num=9999&address=&kill_address=&port=&kill_port=&isp='
    ]
    lua_script = Util.read_lua_script()

    def get_requests(self):
        for url in self.urls:
            yield super().get_request(url)

    def get_proxies(self, response):
        proxy_list = response.xpath("//div[@class='layui-row layui-col-space15']/div/div/div/text()").extract()
        for row in proxy_list:
            row = row.strip()
            if re.match(super().PATTERN, row):
                pi = ProxyItem()
                pi['host'] = row.split(':')[0]
                pi['port'] = row.split(':')[1]
                pi['_type'] = 0
                pi['ping'] = None
                yield pi


    def get_next(self, response):
        return None
