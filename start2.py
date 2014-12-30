__author__ = 'shellbye'
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from zhihu.spiders.user_profile import UserProfileSpider
from scrapy.utils.project import get_project_settings
from pymongo import MongoClient

from wsc.settings import IP, DB


# def start_spider(user_data_id):
spider = UserProfileSpider(user_data_id=user_data_id)
settings = get_project_settings()
crawler = Crawler(settings)
crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
crawler.configure()
crawler.crawl(spider)
crawler.start()
log.start()
reactor.run()

#
# if __name__ == "__main__":
#     zhihu_user_data_ids = MongoClient(IP, 27017)[DB]['zhihu_user_data_ids']
#     count = 0
#     while True:
#         count += 1
#         user = zhihu_user_data_ids.find_one({"crawled": False},
#                                             {"user_data_id": 1, "_id": 0})
#         # print user['user_data_id']
#         if not user:
#             break
#         start_spider(user['user_data_id'])
#         if count > 5:
#             break