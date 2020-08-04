import unittest
from scrapy.http import HtmlResponse
from proxy_collector_scrapy.providers.PremProxy import PremProxy
from proxy_collector_scrapy.items import ProxyItem
import os

HTML_PAGE = os.path.join(os.path.dirname(__file__), 'html-files/page1.html')


class TestPremProxy(unittest.TestCase):
    html_page = None
    pp = PremProxy()
    p1 = ProxyItem()
    p2 = ProxyItem()
    p3 = ProxyItem()

    def setUp(self):
        super().setUp()
        f = open(HTML_PAGE, 'rb')
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

    def test_get_proxies(self):
        res = self.pp.get_proxies(self.html_page)
        self.assertEqual(res[0], self.p1)
        self.assertEqual(res[1], self.p2)
        self.assertEqual(res[2], self.p3)


if __name__ == '__main__':
    unittest.main()