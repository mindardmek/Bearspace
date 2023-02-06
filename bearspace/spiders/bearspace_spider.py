import scrapy
from bearspace.items import ProductItem
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess

# Defines a Spider class
class BearspaceSpider(scrapy.Spider):
    name = 'bearspace_spider'
    start_urls = ['https://www.bearspace.co.uk/purchase?page=1']

    # Sets custom output settings for the spider
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'output.csv'
    }

    # Defines the parse method
    def parse(self, response):
        # Finds all products on the page using XPath selector
        products_list = response.xpath(
            '//li[@data-hook="product-list-grid-item"]')
        # Checks if a list of products exist on the page 
        if not products_list:
            return
        # Loops over all the products in products_list
        for product in products_list:
            # Extracts URL for each product in products_list
            product_url = product.xpath(
                './/div[contains(@class, "ETPbIy")]/a/@href').get()
            # Sends a request to the product URL and calls parse_product method for each product 
            if product_url:
                yield scrapy.Request(response.urljoin(product_url), callback=self.parse_product)

        # Increments the page number and create a new request
        page_number = int(response.url.split('=')[-1]) + 1
        next_page = f'https://www.bearspace.co.uk/purchase?page={page_number}'
        yield scrapy.Request(next_page, callback=self.parse)

    # Defines the parse_product method to extract product information from the product page
    def parse_product(self, response):
         # Initializes an ItemLoader object for the ProductItem
        loader = ItemLoader(item=ProductItem(), selector=response)
        # Adds product information to the loader
        loader.add_value(
            'product_url', response.url)
        loader.add_xpath(
            'title', './/h1[@data-hook="product-title"]/text()')
        loader.add_xpath(
            'media', './/section[@data-hook="description-wrapper"]//*[text()]/text()')
        loader.add_xpath(
            'height_cm', './/section[@data-hook="description-wrapper"]//*[text()]/text()')
        loader.add_xpath(
            'width_cm', './/section[@data-hook="description-wrapper"]//*[text()]/text()')
        loader.add_xpath(
            'price_gbp', './/div[@data-hook="product-price"]//span[1]/text()')
        # Yields items in the loader
        yield loader.load_item()

# Run scrapy crawl in the terminal 
    #scrapy crawl bearspace_spider -O output.csv

#process = CrawlerProcess()
#process.crawl(BearspaceSpider)
#process.start()


