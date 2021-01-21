# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from scrapy import Field, Item


class YellowpagesItem(Item):
    # define the fields for your item here like:
    name = Field()
    mail = Field()
    number = Field()
    website = Field()
    country = Field()
    industry = Field()
