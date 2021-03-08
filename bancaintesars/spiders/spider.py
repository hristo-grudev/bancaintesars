import scrapy

from scrapy.loader import ItemLoader
from w3lib.html import remove_tags

from ..items import BancaintesarsItem
from itemloaders.processors import TakeFirst


class BancaintesarsSpider(scrapy.Spider):
	name = 'bancaintesars'
	start_urls = ['https://www.bancaintesa.rs/medija-centar/vesti.361.html']

	def parse(self, response):
		post_links = response.xpath('//p[@class="more"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//li[@class="next"]/a/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//article//p//text()[normalize-space() and not(ancestor::a | ancestor::p[@class="posted"])]').getall()
		description = [remove_tags(p).strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//p[@class="posted"]/text()').get()

		item = ItemLoader(item=BancaintesarsItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
