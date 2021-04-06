import scrapy

from scrapy.loader import ItemLoader

from ..items import FcbankingItem
from itemloaders.processors import TakeFirst


class FcbankingSpider(scrapy.Spider):
	name = 'fcbanking'
	start_urls = ['https://www.fcbanking.com/why-us/press-releases/']

	def parse(self, response):
		post_links = response.xpath('//a[text()="Continue reading"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "lowercase", " " ))]/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		if not title:
			return
		description = response.xpath('//article//div[@class="body "]//text()[normalize-space() and not(ancestor::h1)]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()

		item = ItemLoader(item=FcbankingItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)

		return item.load_item()
