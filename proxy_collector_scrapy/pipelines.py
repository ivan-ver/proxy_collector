# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from proxy_collector_scrapy.utils.data_base import Database


class ProxyCollectorScrapyPipeline(object):
    flush_count = 5
    items = set()

    def open_spider(self, spider):
        if spider.name == 'get_unchecked':
            with Database() as db:
                db.truncate_unchecked()

    def close_spider(self, spider):
        with Database() as db:
            db.save_unchecked(self.items)


    def process_item(self, item, spider):
        self.items.add(item)
        if len(self.items) > self.flush_count:
            with Database() as db:
                db.save_unchecked(self.items)
            self.items.clear()
        return item



