import scrapy
import datetime,re
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from myhome.items import MyhomeItem


class MyhomeSpider(CrawlSpider):
    name = "myhomesale"
    allowed_domains = ["myhome.ie"]
    start_urls = [
        "http://myhome.ie/residential/ireland/property-for-sale"
    ]
    rules = (
        Rule(LinkExtractor(allow=(r'\?page=\d+'))),
        Rule(LinkExtractor(allow=(r'/brochure/.+\/\d+')),callback="parse_item"),
    )
