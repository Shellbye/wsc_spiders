# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo.mongo_client import MongoClient
import settings


class ZhihuPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoDBPipelineSimplified(object):

    def __init__(self):
        self.connection = MongoClient(settings.MONGODB_URI)
        self.database = self.connection[settings.MONGODB_DATABASE]
        self.collection = None

    def process_item(self, item, spider):
        self.collection = self.database[spider.name]
        if not isinstance(item, list):
            item = dict(item)
        self.collection.insert(item, continue_on_error=True)
        return item