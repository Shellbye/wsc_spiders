# -*- coding: utf-8 -*-

# Scrapy settings for zhihu project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
ITEM_PIPELINES = {
    'scrapy_mongodb.MongoDBPipeline': 300,
    # 'lagou.scrapy_mysql_v0.MySQLPipeline': 5,
    # 'lagou.scrapy_mongodb_simplified.MongoDBPipelineSimplified': 55,
    # 'scrapy.contrib.pipeline.images.ImagesPipeline': 1,
}

BOT_NAME = 'zhihu'

SPIDER_MODULES = ['zhihu.spiders']
NEWSPIDER_MODULE = 'zhihu.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'zhihu (+http://www.yourdomain.com)'
MONGODB_URI = 'mongodb://192.168.2.222:27017'
MONGODB_DATABASE = 'scrapy'
MONGODB_COLLECTION = 'zhihu'

LOG_FILE = 'zhihu.log'
LOG_LEVEL = 'INFO'

COOKIES_ENABLES = True