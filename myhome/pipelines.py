# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3
from os import path
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

class MyhomePipeline(object):
    def process_item(self, item, spider):
        return item

# 验证数据
from scrapy.exceptions import DropItem
class PricePipeline(object):
# 	"""docstring for PricePipeline"""
# 	# vat_factor=1.5
	def process_item(self, item, spider):
# 		# if item['deposit']:
# 		# 	if item['price-excludes-vat']:
# 		# 	item['deposit'] *= self.vat_factor
		return item
		# else:
		# 	raise DropItem('Missing deposit in %s' % item)


# 写Json文件
import json
class JsonWriterPipeline(object):
	"""docstring for ClassName"""
	def __init__(self):
		self.file = open('items3.jl','wb')

	def process_item(self, item, spider):
		line = json.dumps(dict(item)) + '\n'
		self.file.write(line)
		return item

# 检查重复
# from scrapy.exceptions import DropItem
# class DuplicatesPipeline(object):
# 	"""docstring for Duplicate"""
# 	def __init__(self):
# 		self.urls_seen = set()
# 	def process_item(self, item, spider):
# 		if item['url'] in self.urls_seen:
# 			raise DropItem("Duplicate item found: %s" % item)
# 		else:
# 			self.urls_seen.add(item['url'])
# 			return item


# Write items to SQLite
class SqlitePipeline(object):
	filename='data.db'

	def __init__(self):
		self.conn = None
		dispatcher.connect(self.initialize, signals.engine_started)
		dispatcher.connect(self.finalize, signals.engine_stopped)

	def process_item(self,item,spider):
		self.conn.execute("insert into Myhome values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
		                  (item['url'],item['address'],
		                  item['rentPrice'],item['currencyCode'],item['deposit'],
		               	  item['leaseTerm'],item['addedOnDate'],item['beds'],
		               	  item['description'],item['negotiator'],item['agentName'],
		               	  item['agentAddress'],item['agentPhone'],item['agentFax'],
		               	  item['agentLicence'],item['latitude'],item['longitude'],
		               	  item['ber'],item['ber_detail'],item['features'],
		               	  item['image_urls'],item['landlordPhone'],item['shortLink'],
		               	  item['services_in_this_area']))
		return item

	def initialize(self):
		if path.exists(self.filename):
			self.conn = sqlite3.connect(self.filename)
		else:
			self.conn = self.create_table(self.filename)

	def finalize(self):
		if self.conn is not None:
			self.conn.commit()
			self.conn.close()
			self.conn = None

	def create_table(self,filename):
		conn = sqlite3.connect(filename)
		conn.execute('''create table Myhome
					(url string primary key, address string, 
					 rentPrice decimal, currencyCode unicode, 
					 deposit decimal, leaseTerm string, 
					 addedOnDate string, beds integer, 
					 description string, negotiator string, 
					 agentName string, agentAddress string, 
					 agentPhone string, agentFax string, 
					 agentLicence string, latitude decimal, 
					 longitude decimal, ber string, ber_detail string, 
					 features string, image_urls string, 
					 landlordPhone string, shortLink string, 
					 services_in_this_area string)''')
		# conn.execute('SELECT * FROM Myhome')
		conn.commit()
		return conn


# Write items to MongoDB
# import pymongo

# class MongoPipeline(object):
# 	"""docstring for  """
# 	def __init__(self, mongo_uri, mongo_db):
# 		self.mongo_uri = mongo_uri
# 		self.mongo_db = mongo_db

# 	@classmethod
# 	def from_crawler(cls, crawler):
# 		return cls(
# 			mongo_uri=crawler.settings.get('MONGO_URI'),
# 			mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
# 		)
	
# 	def open_spider(self, spider):
# 		self.client = pymongo.MongoClient(self.mongo_uri)
# 		self.db = self.client[self.mongo_db]

# 	def close_spider(self, spider):
# 		self.client.close()

# 	def process_item(self, item, spider):
# 		self.db[self.collecton_name].insert(dict(item))
# 		return item
		


