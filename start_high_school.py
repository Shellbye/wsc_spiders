#!/usr/bin/env python
__author__ = 'shellbye'
import logging
logging.basicConfig(filename='start.err.log', level=logging.DEBUG)

from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from school.spiders.high_school import HighSchoolSpider
from scrapy.utils.project import get_project_settings


def setup_spider():
    spider = HighSchoolSpider()
    settings = get_project_settings()
    crawler = Crawler(settings)
    crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()


def start():
    setup_spider()
    logging.log(logging.INFO, "setup high_school")
    log.start()
    reactor.run()


if __name__ == "__main__":
    start()