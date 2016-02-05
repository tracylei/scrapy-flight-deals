import scrapy
from scrapy_flight_deals.items import FlightDealItem

class FlightDealsSpider(scrapy.Spider):
	name = "yyzDeals"
	allowed_domains = ["yyzdeals.com"]
	start_urls = ["http://yyzdeals.com/"]

	def parseCost (self, title):
		# Split on space
		title = title[0].split()
		for word in title:
			if word[0] == '$':
				return int(word[1:])

	def parse(self, response):
		for deal in response.xpath('//div[@id="contentleft"]//h1'):
			item = FlightDealItem()
			item['postTitle']	= deal.xpath('a/text()').extract()
			item['postDay']		= deal.xpath('div[@class="cal"]/span[@class="calday"]/text()').extract()
			item['postMonth']	= deal.xpath('div[@class="cal"]/span[@class="calmonth"]/text()').extract()
			item['postYear']	= deal.xpath('div[@class="cal"]/span[@class="calyear"]/text()').extract()
    		item['cost']			= self.parseCost(item['postTitle'])
    		item['destinations']	= item['postTitle']
    		item['link']		= deal.xpath('a/@href').extract()
    		yield item

