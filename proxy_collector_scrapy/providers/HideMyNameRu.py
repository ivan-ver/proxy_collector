from proxy_collector_scrapy.items import ProxyItem
from proxy_collector_scrapy.providers.Provider import Provider


class HideMyNameRu(Provider):
    urls = ['https://hidemy.name/ru/proxy-list/?country=ALARAMAZBDBYBEBJBOBWBRBGKHCMCACLCOCGCDCRHRCYCZDOECEGGQFIFRGEDEGHGRGTHNHKHUINIDIRIQIEITJPKZKEKRKGLBLYLTMWMYMVMUMXMDMNMENPNLNINGNOPKPSPEPLPRRORURSSLSGSKSISOZAESSECHSYTWTZTHTRUGUAGBUSVNZMZW#list']
    main_url = 'https://hidemy.name'
    def get_requests(self):
        for url in self.urls:
            yield super().get_request(url)

    def get_proxies(self, response):
        r = response
        table = r.xpath("//div[@class='table_block']/table//tr")[1:]
        for row in table:
            try:
                pi = ProxyItem()
                pi['host'] = row.xpath("td[1]/text()").get()
                pi['port'] = row.xpath("td[2]/text()").get()
                if 'https' in row.xpath("td[5]/text()").get().lower():
                    pi['_type'] = 2
                elif 'http' in row.xpath("td[5]/text()").get().lower():
                    pi['_type'] = 1
                elif 'socks4' in row.xpath("td[5]/text()").get().lower():
                    pi['_type'] = 3
                elif 'socks5' in row.xpath("td[5]/text()").get().lower():
                    pi['_type'] = 4
                else:
                    pi['_type'] = 0
                pi['ping'] = None
                yield pi
            except:
                continue



    def get_next(self, response):
        next_page = response.xpath("//div[@class='pagination']//li[@class='next_array']/a/@href").get()
        if next_page:
            return self.get_request(self.main_url + next_page)
        else:
            return None
