# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class YellowpagesPipeline:
    def process_item(self, item, spider):
        return item

class DuplicateItemFilter:
    def __init__(self):
        self.item_codes_seen = set()
    def process_item(self, item, spider):
        if item['item_code'] in self.item_codes_seen:
            raise DropItem("Duplicate item found: %s" %
            item['item_code'])
        self.item_codes_seen.add(item['item_code'])
        return item