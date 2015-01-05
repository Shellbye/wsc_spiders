#!/usr/bin/env python
__author__ = 'shellbye'
import time

from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from zhihu.spiders.user_profile import UserProfileSpider
from scrapy.utils.project import get_project_settings
from pymongo import MongoClient

from wsc.settings import IP, DB


class ReactorControl:

    def __init__(self):
        self.crawlers_running = 0

    def add_crawler(self):
        self.crawlers_running += 1

    def remove_crawler(self):
        self.crawlers_running -= 1
        if self.crawlers_running == 0:
            reactor.stop()
            # print "stop reactor..."
            # time.sleep(10)
            # sc = SpiderControl()
            # sc.start()


class SpiderControl():
    def __init__(self):
        self.zhihu_user_data_ids = MongoClient(IP, 27017)[DB]['zhihu_user_data_ids']
        self.count = 0
        self.control = ReactorControl()

    def setup_spider(self, user_data_id):
        spider = UserProfileSpider(user_data_id=user_data_id)
        settings = get_project_settings()
        log.start_from_settings(settings)
        crawler = Crawler(settings)
        crawler.signals.connect(self.control.remove_crawler, signal=signals.spider_closed)
        crawler.configure()
        crawler.crawl(spider)
        self.control.add_crawler()
        crawler.start()

    def start(self):
        self.count = 0
        while True:
            self.count += 1
            user = self.zhihu_user_data_ids.find_one({"fetched": False})
            if not user:
                user = self.zhihu_user_data_ids.find_one({"crawled_successfully": False})
                if not user:
                    raise TypeError("No data available in Mongo")
            crawled_count = user['crawled_count'] + 1
            self.zhihu_user_data_ids.update(
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
            self.setup_spider(user['user_data_id'])
            if self.count >= 5:
                break
        log.start()
        reactor.run()


if __name__ == "__main__":
    sc = SpiderControl()
    sc.start()