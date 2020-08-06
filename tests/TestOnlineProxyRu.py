import unittest
from scrapy.http import HtmlResponse
from proxy_collector_scrapy.providers.OnlineProxyRu import OnlineProxyRu
from proxy_collector_scrapy.items import ProxyItem
import os
WAY = os.path.dirname(__file__)


class TestOnlineProxyRu(unittest.TestCase):
    html_page = None
    pp = OnlineProxyRu()
    p1 = ProxyItem()
    p2 = ProxyItem()
    p3 = ProxyItem()

    def setUp(self):
        f = open(WAY + '/html-files/OnlineProxyRu.html', 'rb')
        text = f.read()
        f.close()
        self.html_page = HtmlResponse(url='', body=text)

        self.p1["host"] = "37.205.48.116"
        self.p1["port"] = "8080"
        self.p1["_type"] = 3
        self.p1["ping"] = 90

        self.p2["host"] = "95.183.73.89"
        self.p2["port"] = "8080"
        self.p2["_type"] = 3
        self.p2["ping"] = 146

        self.p3["host"] = "185.75.67.237"
        self.p3["port"] = "8080"
        self.p3["_type"] = 3
        self.p3["ping"] = 33

    def test_get_proxies(self):
        res = [i for i in self.pp.get_proxies(self.html_page)]
        self.assertEqual(res[0], self.p1)
        self.assertEqual(res[1], self.p2)
        self.assertEqual(res[2], self.p3)


if __name__ == '__main__':
    unittest.main()