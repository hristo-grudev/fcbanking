import scrapy


class FcbankingItem(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()
