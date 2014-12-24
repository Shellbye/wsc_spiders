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
    locations = scrapy.Field()
    business = scrapy.Field()
    business_topic_url = scrapy.Field()
    gender = scrapy.Field()
    employments = scrapy.Field()
    educations = scrapy.Field()
    description = scrapy.Field()
    agree_count = scrapy.Field()
    thanks_count = scrapy.Field()
    weibo_url = scrapy.Field()
    followee_count = scrapy.Field()
    follower_count = scrapy.Field()
    questions_count = scrapy.Field()
    answers_count = scrapy.Field()
    posts_count = scrapy.Field()
    collections_count = scrapy.Field()
    logs_count = scrapy.Field()
    personal_page_view_count = scrapy.Field()
    follow_columns_count = scrapy.Field()
    follow_topics_count = scrapy.Field()
    questions = scrapy.Field()
    answers = scrapy.Field()