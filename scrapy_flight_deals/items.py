import scrapy


class FlightDealItem(scrapy.Item):

    postTitle				= scrapy.Field()
    postDay					= scrapy.Field()
    postMonth				= scrapy.Field()
    postYear				= scrapy.Field()
    cost					= scrapy.Field()
    destinationCountries	= scrapy.Field()
    destinationCities		= scrapy.Field()
    numDestinations			= scrapy.Field()
    link					= scrapy.Field()
