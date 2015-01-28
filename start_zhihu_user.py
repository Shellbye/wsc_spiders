#!/usr/bin/env python
__author__ = 'shellbye'
import time

from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from zhihu.spiders.user_profile import UserProfileSpider
from scrapy.utils.project import get_project_settings
from pymongo import MongoClient

from wsc.settings import IP, DB, DEBUG


class SpiderControl():
    def __init__(self):
        self.crawlers_running = 0

    def add_crawler(self):
        self.crawlers_running += 1

    def remove_crawler(self):
        self.crawlers_running -= 1
        if self.crawlers_running == 0:
            reactor.stop()

    def setup_spider(self, user_data_id):
        spider = UserProfileSpider(user_data_id=user_data_id)
        settings = get_project_settings()
        crawler = Crawler(settings)
        crawler.signals.connect(self.remove_crawler, signal=signals.spider_closed)
        crawler.configure()
        crawler.crawl(spider)
        self.add_crawler()
        crawler.start()


def start():
    zhihu_user_data_ids = MongoClient(IP, 27017)[DB]['zhihu_user_data_ids']
    user_profile = MongoClient(IP, 27017)[DB]['user_profile']
    count = 0
    while True:
        count += 1
        user = zhihu_user_data_ids.find_one({"fetched": False})
        if not user:
            user = zhihu_user_data_ids.find_one({"crawled_successfully": False})
            if not user:
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
            break
        the_user = user_profile.find({"user_data_id": user['user_data_id']})
        if the_user.count() > 0:
            continue
        sc = SpiderControl()
        sc.setup_spider(user['user_data_id'])
        if DEBUG:
            ceil = 3
        else:
            ceil = 500
        if count >= ceil:
            break
    log.start()
    reactor.run()


if __name__ == "__main__":
    start()