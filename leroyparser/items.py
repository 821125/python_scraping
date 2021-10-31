# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst


class LeroyparserItem(scrapy.Item):
    title = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(output_processor=TakeFirst())
    link = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(lambda x: int(x.strip())), output_processor=TakeFirst())
    _id = scrapy.Field()
