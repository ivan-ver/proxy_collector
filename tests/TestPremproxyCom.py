import unittest
from scrapy.http import HtmlResponse
from proxy_collector_scrapy.providers.PremproxyCom import PremproxyCom
from proxy_collector_scrapy.items import ProxyItem
import os
WAY = os.path.dirname(__file__)


class TestPremProxy(unittest.TestCase):
    html_page = None
    next_page = None
    no_next_page = None
    pp = PremproxyCom()
    p1 = ProxyItem()
    p2 = ProxyItem()
    p3 = ProxyItem()

    def setUp(self):
        f = open(WAY + '/html-files/PremProxyComGetReq.html', 'rb')
        text = f.read()
        f.close()

        self.html_page = HtmlResponse(url='', body=text)

        self.p1["host"] = "118.32.118.60"
        self.p1["port"] = "3128"
        self.p1["_type"] = 1
        self.p1["ping"] = None

        self.p2["host"] = "217.219.61.6"
        self.p2["port"] = "8080"
        self.p2["_type"] = 1
        self.p2["ping"] = None

        self.p3["host"] = "84.210.183.13"
        self.p3["port"] = "3128"
        self.p3["_type"] = 1
        self.p3["ping"] = None

        with open(WAY + '/html-files/PremProxyComNextPage.html', 'rb') as p:
            self.next_page = HtmlResponse(url='', body=p.read())
        with open(WAY + '/html-files/PremProxyComNoNextPage.html', 'rb') as p:
            self.no_next_page = HtmlResponse(url='', body=p.read())

    def test_get_proxies(self):
        res = [i for i in self.pp.get_proxies(self.html_page)]
        self.assertEqual(res[0], self.p1)
        self.assertEqual(res[1], self.p2)
        self.assertEqual(res[2], self.p3)

    def test_get_next(self):
        res_next_url = self.pp.get_next(self.next_page)
        self.assertEqual(res_next_url.url, 'http://premproxy.com/list/02.htm')
        res_no_next_url = self.pp.get_next(self.no_next_page)
        self.assertEqual(res_no_next_url, None)


if __name__ == '__main__':
    unittest.main()