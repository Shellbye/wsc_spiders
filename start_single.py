#!/usr/bin/env python
__author__ = 'shellbye'
import time
import logging
logging.basicConfig(filename='start.err.log', level=logging.DEBUG)

from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from zhihu.spiders.user_profile import UserProfileSpider
from scrapy.utils.project import get_project_settings
from pymongo import MongoClient

from wsc.settings import IP, DB


def setup_spider(user_data_id):
    spider = UserProfileSpider(user_data_id=user_data_id)
    settings = get_project_settings()
    crawler = Crawler(settings)
    crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()


def start():
    zhihu_user_data_ids = MongoClient(IP, 27017)[DB]['zhihu_user_data_ids']
    user_profile = MongoClient(IP, 27017)[DB]['user_profile']
    user = zhihu_user_data_ids.find_one({"fetched": False})
    if not user:
        logging.log(logging.WARNING, "no more fetched:false")
        user = zhihu_user_data_ids.find_one({"crawled_successfully": False})
        if not user:
            logging.log(logging.WARNING, "no more crawled_successfully:false")
            raise TypeError("No data available in Mongo")
    crawled_count = user['crawled_count'] + 1
    zhihu_user_data_ids.update(
        user,
        {
            "$set":
                {
                    "fetched": True,
                    "last_crawled_time": time.strftime("%Y-%m-%d:%H:%M:%S"),
                    "crawled_count": crawled_count,
                }
        }
    )
    if not user:
        return
    the_user = user_profile.find({"user_data_id": user['user_data_id']})
    if the_user.count() > 0:
        return
    setup_spider(user['user_data_id'])
    logging.log(logging.INFO, "setup " + user['user_data_id'])
    log.start()
    reactor.run()


if __name__ == "__main__":
    start()