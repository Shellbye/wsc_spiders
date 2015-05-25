# -*- coding: utf-8 -*-

# Scrapy settings for wsc project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'wsc'
DEBUG = True
PROXY_ENABLED = False
NEED_LOGIN = False

SPIDER_MODULES = ['wsc.spiders',
                  'zhihu.spiders',
                  'lagou.spiders',
                  'kanzhun.spiders',
                  'school.spiders',
                  'sina.spiders',
                  'ganji.spiders',
                  ]
NEWSPIDER_MODULE = 'wsc.spiders'

IP = "192.168.3.222"

MONGODB_URI = 'mongodb://' + IP + ':27017'
MONGODB_DATABASE = 'user'

DB = MONGODB_DATABASE

ITEM_PIPELINES = {
    'wsc.pipelines.MongoDBPipeline': 300,
}

LOG_FILE = 'wsc.log'
if DEBUG:
    LOG_LEVEL = 'DEBUG'
else:
    LOG_LEVEL = 'WARNING'

COOKIES_ENABLES = True
COOKIES_DEBUG = True

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'wsc.rotate_useragent.RotateUserAgentMiddleware': 400,
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 500,
    # 'wsc.proxy.ProxyMiddleware': 510,
}

if PROXY_ENABLED:
    DOWNLOADER_MIDDLEWARES['wsc.proxy.ProxyMiddleware'] = 510

WEBSERVICE_RESOURCES = {
    'wsc.services.ItemResource.ItemCountResource': 1,
}

EXTENSIONS = {
    'scrapy.telnet.TelnetConsole': None,
}

# DOWNLOAD_DELAY = 10