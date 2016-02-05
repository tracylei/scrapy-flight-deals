import scrapy
from scrapy_flight_deals.items import FlightDealItem
import geograpy

HOME_CITY 		= 'Toronto'
HOME_COUNTRY	= 'Canada'

class FlightDealsSpider(scrapy.Spider):

	name = "yyzDeals"
	allowed_domains = ["yyzdeals.com"]
	start_urls = ["http://yyzdeals.com/"]

	def parseCost (self, title):
		# Split on space
		title = title.split()
		for word in title:
			if word[0] == '$':
				return int(word[1:])

	def parseCountries (self, title):
		countries 		= geograpy.get_place_context(text=title).countries
		newCountries 	= []
		for country in countries:
			if country != HOME_COUNTRY:
				newCountries.append(country)
		return newCountries

	def parseCities (self, title):
		cities 		= geograpy.get_place_context(text=title).cities
		newCities 	= []
		for city in cities:
			if city != HOME_CITY:
				newCities.append(city)
		return newCities

	def countDestinations (self, cities, countries, title):
		# Assumption s: the occurrence of "or" indicates there is only one destination
		title = title.split()
		orExists = 0
		for word in title:
			if word == 'or':
				orExists = 1
		if orExists:
			return 1
		return max(len(cities), len(countries)))

	def parse (self, response):
		for deal in response.xpath('//div[@id="contentleft"]/h1'):
			item = FlightDealItem()
			item['postTitle']				= deal.xpath('a/text()').extract()
			item['postDay']					= deal.xpath('div[@class="cal"]/span[@class="calday"]/text()').extract()
			item['postMonth']				= deal.xpath('div[@class="cal"]/span[@class="calmonth"]/text()').extract()
			item['postYear']				= deal.xpath('div[@class="cal"]/span[@class="calyear"]/text()').extract()
			item['cost']					= self.parseCost(item['postTitle'][0])
			item['destinationCountries']	= self.parseCountries(item['postTitle'][0])
			item['destinationCities']		= self.parseCities(item['postTitle'][0])
			item['numDestinations']			= self.countDestinations(
															item['destinationCities'],
															item['destinationCountries'],
															item['postTitle'][0])
			item['link']					= deal.xpath('a/@href').extract()
			yield item
		next_page = response.xpath("//p/a[@class='next-page']/@href")
		if next_page:
			url = response.urljoin(next_page[0].extract())
			yield scrapy.Request(url, self.parse)
