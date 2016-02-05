Crawl yyzdeals for past flight deals.

To start the spider, run
```
scrapy crawl yyzDeals -o deals.json
```
A file called **deals.json** will be created with the deals found in json format.

Make sure you have the **geograpy** library installed.

To-dos:
- account for "or" in title when counting number of destinations
- account for "or" used with "with"
- United States & Australia being detected in most titles without US/Australian destinations
- Detecting continents
- Consider parsing article tags instead
