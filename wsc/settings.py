# -*- coding: utf-8 -*-

# Scrapy settings for wsc project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'wsc'

SPIDER_MODULES = ['wsc.spiders', 'zhihu.spiders', 'lagou.spiders']
NEWSPIDER_MODULE = 'wsc.spiders'

MONGODB_URI = 'mongodb://192.168.2.222:27017'
MONGODB_DATABASE = 'scrapy'
MONGODB_COLLECTION = 'wsc'

ITEM_PIPELINES = {
    'wsc.pipelines.MongoDBPipeline': 300,
}

LOG_FILE = 'wsc.log'
LOG_LEVEL = 'INFO'

COOKIES_ENABLES = True

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'wsc.rotate_useragent.RotateUserAgentMiddleware': 400
}

WEBSERVICE_RESOURCES = {
    'wsc.services.ItemResource.ItemCountResource': 1,
}