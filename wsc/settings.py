# -*- coding: utf-8 -*-

# Scrapy settings for wsc project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'wsc'
DEBUG = False

SPIDER_MODULES = ['wsc.spiders', 'zhihu.spiders', 'lagou.spiders']
NEWSPIDER_MODULE = 'wsc.spiders'

IP = "localhost"

MONGODB_URI = 'mongodb://' + IP + ':27017'
MONGODB_DATABASE = 'scrapy2'
MONGODB_COLLECTION = 'wsc'

DB = MONGODB_DATABASE

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

EXTENSIONS = {
    'scrapy.telnet.TelnetConsole': None,
}

if DEBUG:
    pass
else:
    DOWNLOAD_DELAY = 1