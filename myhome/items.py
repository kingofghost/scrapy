# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MyhomeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    address = scrapy.Field()
    rentPrice = scrapy.Field()
    SellPrice = scrapy.Field()
    # price-excludes-vat = scrapy.Field()
    currencyCode = scrapy.Field()
    deposit = scrapy.Field()
    size = scrapy.Field()
    leaseTerm = scrapy.Field()
    addedOnDate = scrapy.Field()
    beds = scrapy.Field()
    # property_type = scrapy.Field()
    description = scrapy.Field()
    negotiator = scrapy.Field()
    agentName = scrapy.Field()
    agentAddress = scrapy.Field()
    agentPhone = scrapy.Field()
    agentFax = scrapy.Field()
    agentLicence = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    ber = scrapy.Field()
    ber_detail = scrapy.Field()
    features = scrapy.Field()
    image_urls = scrapy.Field()
    landlordPhone = scrapy.Field()
    shortLink = scrapy.Field()
    accomodation = scrapy.Field()
    viewing = scrapy.Field()
    service_charge = scrapy.Field()
    directions = scrapy.Field()
    services_in_this_area = scrapy.Field()

    # similarProperties = scrapy.Field()
    
    # beds = scrapy.Field()
    # baths = scrapy.Field()
    # status = scrapy.Field()
    # date_entered = scrapy.Field()
    # contact_phone = scrapy.Field()
    # url = scrapy.Field()
    # agency = scrapy.Field()
    # is_private = scrapy.Field()
    
    # image_urls = scrapy.Field()
    # images = scrapy.Field()
    # latitude = scrapy.Field()
    # longitude = scrapy.Field()
    # ber = scrapy.Field()
    # pass
    

# class TorrentItem(scrapy.Item):
#     url = scrapy.Field()
#     name = scrapy.Field()
#     description = scrapy.Field()
#     size = scrapy.Field()