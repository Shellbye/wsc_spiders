# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhihuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ZhiHuUserProfile(scrapy.Item):
    user_data_id = scrapy.Field()
    name = scrapy.Field()
    url_name = scrapy.Field()
    bio = scrapy.Field()
    location = scrapy.Field()
    business = scrapy.Field()
    business_topic_url = scrapy.Field()
    gender = scrapy.Field()
    employment = scrapy.Field()
    position = scrapy.Field()
    description = scrapy.Field()
    agree_count = scrapy.Field()
    thanks_count = scrapy.Field()
    weibo_url = scrapy.Field()