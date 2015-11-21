#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import scrapy
import datetime
import re
import logging
import locale
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from myhome.items import MyhomeItem


class MyhomeSpider(CrawlSpider):
    name = "rent"
    allowed_domains = ["myhome.ie"]
    start_urls = [
        "http://myhome.ie/rentals/ireland/property-to-rent"
    ]
    rules = (
        Rule(LinkExtractor(allow=(r'\?page=\d+'))),
        Rule(LinkExtractor(allow=(r'/brochure/.+\/\d+')),callback="parse_item"),
    )

    # def parse(self, response):
    #     for sel in response.xpath('//ul[@id="results"]'):
    #         address = sel.xpath('li/div/div/a/text()').extract()
    #         # rentPrice = sel.xpath('span[@class="rentPrice"]/text()').extract()
    #         # property_type = sel.xpath('div[@class="descriptionTitle "]').extract()
    #         # description = sel.xpath('div[@class="description "]').extract()
    #         # url = sel.xpath('a/@href').extract()

    #         print address
    #          # rentPrice, property_type, description

    def parse_item(self, response):
        sel = Selector(response)
        item = MyhomeItem()
        item['url'] =  response.url
        # item['address'] = sel.xpath('//*[@class="brochureAddress"]/text()').extract()
        item['address'] = self.get_address(response)
        # item['rentPrice'] = sel.xpath('//*[@class="brochureDescription"]/div/text()').extract()
        item['rentPrice'] = self.get_rentPrice(response)
        item['currencyCode'] = self.get_currencyCode(response)
        item['deposit'] = self.get_deposit(response)
        item['leaseTerm'] = self.get_leaseTerm(response)
        item['addedOnDate'] = self.get_addedOnDate(response)
        item['beds'] = self.get_beds(response)
        # item['property_type'] = sel.xpath('//*[@class="brochureDescription"]/span/text()').extract()
        # item['property_type'] = self.get_property_type(response)
        # item['description'] = sel.xpath('//*[@class="contentDescription content0"]/text()').extract()
        item['description'] = self.get_description(response)
        # item['similarProperties'] = sel.xpath('//*[@id="similarProperties"]/div/h4/text()').extract()
        # item['negotiator'] = sel.xpath('//*[@class="negotiator"]/text()').extract()
        item['negotiator'] = self.get_negotiator(response)
        # item['agentName'] = sel.xpath('//*[@class="agentName"]/a/text()').extract()
        item['agentName'] = self.get_agentName(response)
        # item['agentAddress'] = sel.xpath('//*[@class="agentDetails"]/li[2]/text()').extract()
        item['agentAddress'] = self.get_agentAddress(response)
        # item['agentPhone'] = sel.xpath('//*[@class="agentDetails"]/li/text()').extract()
        item['agentPhone'] = self.get_agentPhone(response)
        # item['agentFax'] = sel.xpath('//*[@class="agentDetails"]/li[4]/text()').extract()
        item['agentFax'] = self.get_agentFax(response)
        item['agentLicence'] = self.get_agentLicence(response)
        # item['latitude'] = sel.xpath('//*[@type="text/javascript"]/text()').re(r'"Latitude":(.?\d+\.\d+)')
        item['latitude'] = self.get_latitude(response)
        item['longitude'] = self.get_longitude(response)
        # item['longitude'] = sel.xpath('//*[@type="text/javascript"]/text()').re(r'"Longitude":(.?\d+\.\d+)')
        # item['ber'] = sel.xpath('//*[@class="contentBER Details content1"]/text()').extract()
        item['ber'] = self.get_ber(response)
        item['ber_detail'] = unicode(self.get_ber_detail(response))
        # item['features'] = sel.xpath('//*[@class="block"]/text()').extract()
        item['features'] = unicode(self.get_features(response))
        item['image_urls'] = unicode(self.get_image_urls(response))
        # item['other'] = sel.css('.brochureText').extract()
        # item['landlordPhone'] = sel.xpath('//*[@class="landlordPhone"]/text()').extract()
        item['landlordPhone'] = self.get_landlordPhone(response)
        item['shortLink'] = sel.xpath('//*[@id="shortLink"]/text()').extract()[0].encode('ascii','ignore')
        # item['viewing'] = sel.xpath('//*[@class=contentViewing Details content3]/text()').extract()
        # item['service_charge'] = sel.xpath('//*[@class="contentService Charge content4"]/text()').extract()
        # item['viewing'] = self.get_viewing(response)
        # item['services_in_this_area'] = sel.xpath('//a[contains(@href,"/services/")]/text()').extract()
        item['services_in_this_area'] = unicode(self.get_services_in_this_area(response))
        # for item in items:
        #     items.append() = sel.xpath('//*[@class="brochureAddress]/text()').extract()
        return item

#     def get_features(self,response):
#         other_div = response.xpath('//*[@class="brochureText"]').extract()
#         if other_div:
#             div_text = other_div[0]
#             m = re.search('(<h3>Features</h3>.+<span class="block">(\w+)</span>.+<span class="block">(\w+)</span>
# ,div_text)
    
    def get_negotiator(self,response):
        negotiator = response.xpath('//*[@class="negotiator"]/text()').extract()
        if negotiator:
            return negotiator[0].encode('ascii','ignore')
        return None

    def get_agentName(self,response):
        agentName = response.xpath('//*[@class="agentName"]/a/text()').extract()
        if agentName:
            return agentName[0].encode('ascii','ignore')
        return None

    def get_agentPhone(self,response):
        agentDetails = response.xpath('//*[@class="agentDetails"]/li/text()').extract()
        if agentDetails:
            for agentDetail in agentDetails:        
                m = re.search(r'Phone:(.+\d+)$',agentDetail)
                if m:
                    agentPhone = m.group(1).strip().encode('ascii','ignore')
                    # agentPhone = re.sub("\s","",agentPhone)
                    # return agentPhone.encode('ascii','ignore')
                    # agentPhone = int(agentPhone)
                    return agentPhone
        return None

    def get_agentFax(self,response):
        agentDetails = response.xpath('//*[@class="agentDetails"]/li/text()').extract()
        if agentDetails:
            for agentDetail in agentDetails:        
                m = re.search(r'Fax:(.+\d+)$',agentDetail)
                if m:
                    agentFax = m.group(1).strip().encode('ascii','ignore')
                    # agentPhone = re.sub("\s","",agentPhone)
                    # return agentPhone.encode('ascii','ignore')
                    # agentPhone = int(agentPhone)
                    return agentFax
        return None

    def get_agentAddress(self,response):
        agentDetails = response.xpath('//*[@class="agentDetails"]/li/text()').extract()
        if agentDetails:
            for agentDetail in agentDetails:
                m = re.search(r'(.+,)+(.+)$',agentDetail)
                if m:
                    agentAddress = m.group().encode('ascii','ignore')
                    return agentAddress
        return None

    def get_agentLicence(self,response):
        agentDetails = response.xpath('//*[@class="agentDetails"]/li/text()').extract()
        if agentDetails:
            for agentDetail in agentDetails:        
                m = re.search(r'Licence:(.+\d+)$',agentDetail)
                if m:
                    agentLicence = m.group(1).strip().encode('ascii','ignore')
                    return agentLicence
        return None
        
    def get_landlordPhone(self,response):
        landlordPhone = response.xpath('//*[@class="landlordPhone"]/text()').extract()
        if landlordPhone:
            return landlordPhone[0].encode('ascii','ignore')
        return None

    def get_image_urls(self,response):
        image_urls = response.xpath('//*[@id="photos"]/li/img/@longdesc').extract()+response.xpath('//*[@id="photos"]/img/@longdesc').extract()
        urls = []
        for image_url in image_urls:
            urls.append('http:'+ image_url.encode('ascii','ignore'))
        return urls

    def get_rentPrice(self,response):
        rentPrice = response.xpath('//*[@class="brochureDescription"]/div/text()').extract()
        m = re.search('\d+|POA',rentPrice[0])
        if m:
            # price = int(price[0].replace(',','').replace(u'\u20ac','').replace('\r\n','').replace('/ month','').replace('/ week','').strip())
            rentPrice = rentPrice[0].replace(',','').replace(u'\u20ac','').replace('\r\n','').strip().encode('ascii','ignore')
        return rentPrice

    def get_currencyCode(self,response):
        currencyCode = response.xpath('//*[@class="brochureDescription"]/div/text()').extract()
        s = currencyCode[0]
        m = re.search(r'(.)\d+,?\d+',s)
        if m:
            # get_currencyCode = map(ord,m.group().decode('hex'))
            # return get_curren(.)\d*,?\d+cyCode
            # code = [ord(c) for c in m.group().decode('hex')]
            # code = []
            # for c in m.group():
            #     code.append(c.decode('hex'))
            # return code.encode('utf-8')
            return m.group(1)
                # return str(i).encode('hex')
        return None

    def get_deposit(self,response):
        deposit = response.xpath('//*[@class="brochureText"]').extract()
        for i in deposit:
            m = re.search(r'Deposit:\s</span>.+?(\d+)',i)
            if m:
                return int(m.group(1).encode('ascii','ignore'))
        return None

    def get_leaseTerm(self,response):
        leaseTerm = response.xpath('//*[@class="block leaseTerm"]/span/text()').extract()
        if leaseTerm:
             return leaseTerm[0].encode('ascii','ignore')
        return None

    def get_addedOnDate(self,response):
        date = response.xpath('//*[@id="propertyAddedOn"]/@title').extract()
        if date:
            return date[0].encode('ascii','ignore')
        return None

    def get_beds(self,response):
        beds = response.xpath('//*[@class="brochureDescription"]/span/text()').extract()
        if beds:
            m = re.search('\d\sBed',beds[0])
            if m:
                beds = int(m.group().replace('Bed','').strip())
                return beds
        return None 

    def get_address(self,response):
        address = response.xpath('//*[@class="brochureAddress"]/text()').extract()
        if address:
            address = address[0].replace('\r\n','').strip().encode('ascii','ignore')
        return address

    def get_description(self,response):
        description = response.xpath('//*[@class="contentDescription content0"]/text()').extract()
        if description:
            description = ','.join(description).encode('ascii','ignore').replace('\r\n','').strip()
            return description
        return None

    def get_features(self,response):
        features = response.xpath('//*[@class="contentFeatures content1"]/text()').extract()+response.xpath('//*[@class="block"]/text()').extract()
        get_features=[]
        for feature in features:
            # m = re.search(r'\\t\\t',feature)
            # n = re.search(r'ac',feature)
            f = feature.replace('\r\n','').strip().encode('ascii','ignore')
            if (re.search(r'\D+',f)):
                get_features.append(f)
        return get_features

    # def get_property_type(self,response):
    #     property_type = response.xpath('//*[@class="brochureDescription"]/span/text()').extract()
    #     if property_type:
    #         property_type = property_type[0].replace('-','').strip().encode('ascii','ignore')
    #         return property_type
    #     return None
 
    def get_ber(self,response):
        ber = response.xpath('//*[@class="brochureDescription"]/img/@alt').extract()
        if ber:
            get_ber = ber[0].encode('ascii','ignore')
            return get_ber
        return None

    def get_ber_detail(self,response):
        raw_data = response.xpath('//*[@class="contentBER Details content1"]/text()').extract()+response.xpath('//*[@class="contentBER Details content2"]/text()').extract()+response.xpath('//*[@class="contentBER Details content3"]/text()').extract()+response.xpath('//*[@class="contentBER Details content4"]/text()').extract()
        ber_detail = []
        # raw_data = response.body.decode(response.encoding).encode('ascii','ignore') 
        # regex_result = re.search('<div class="contentBER Details content\d>\s+(Ber:\s.?',raw_data)
        if raw_data:
            for i in raw_data:
                ber_item = i.replace('\r\n','').strip().encode('ascii','ignore')
                ber_detail.append(ber_item)
            return ber_detail
        return None

    # def get_viewing(self,response):
    #     viewing = response.xpath('//*[@class="contentViewing Information content3"]/text()').extract()
    #     if viewing:
    #         return viewing[0].replace('\r\n','').strip().encode('ascii','ignore')
    #     return None

    def get_latitude(self,response):
        raw_data = response.xpath('//*[@type="text/javascript"]/text()')
        latitude = raw_data.re(r'"Latitude":(.?\d+\.\d+)')
        # latitude=[re.search(r'"Latitude":(.?\d+\.\d+)',i) for i in raw_data]
        if latitude:
            return float(latitude[0].encode('ascii','ignore'))
        return None

    def get_longitude(self,response):
        raw_data = response.xpath('//*[@type="text/javascript"]/text()')
        longitude = raw_data.re(r'"Longitude":(.?\d+\.\d+)')
        if longitude:
            return float(longitude[0].encode('ascii','ignore'))
        return None 

    def get_services_in_this_area(self,response):
        get_services = response.xpath('//a[contains(@href,"/services/")]/text()').extract()
        services = []
        if get_services:
            for i in get_services:
                services.append(i.encode('ascii','ignore'))
            return services
        return None

