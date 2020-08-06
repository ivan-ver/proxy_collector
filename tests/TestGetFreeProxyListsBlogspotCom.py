import unittest
from scrapy.http import HtmlResponse
from proxy_collector_scrapy.providers.MyProxyCom import MyProxyCom
from proxy_collector_scrapy.items import ProxyItem
import os
WAY = os.path.dirname(__file__)


class TestGetFreeProxyListsBlogspotCom(unittest.TestCase):
    html_page = None
    pp = MyProxyCom()
    p1 = ProxyItem()
    p2 = ProxyItem()
    p3 = ProxyItem()

    def setUp(self):
        f = open(WAY + '/html-files/MyProxyComGetReq.html', 'rb')
        text = f.read()
        f.close()
        self.html_page = HtmlResponse(url='', body=text)

        self.p1["host"] = "173.82.78.189"
        self.p1["port"] = "5836"
        self.p1["_type"] = 1
        self.p1["ping"] = None

        self.p2["host"] = "108.61.245.77"
        self.p2["port"] = "8080"
        self.p2["_type"] = 1
        self.p2["ping"] = None

        self.p3["host"] = "191.234.168.144"
        self.p3["port"] = "3128"
        self.p3["_type"] = 1
        self.p3["ping"] = None

    def test_get_proxies(self):
        res = self.pp.get_proxies(self.html_page)
        self.assertEqual(res[0], self.p1)
        self.assertEqual(res[1], self.p2)
        self.assertEqual(res[2], self.p3)


if __name__ == '__main__':
    unittest.main()