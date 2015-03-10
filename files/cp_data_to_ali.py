__author__ = 'shellbye'
import time
import logging
from pymongo.errors import DuplicateKeyError
from pymongo import MongoClient
local_ip = '192.168.2.222'
remote_ip = '218.244.136.252'
logging.basicConfig(filename='cp_data_to_ali.log', level=logging.DEBUG)


def cp_data():

    pass


if __name__ == "__main__":
    local_zhihu_user_data_ids = MongoClient(local_ip, 27017)['scrapy2']['zhihu_user_data_ids']
    # local_questions = MongoClient(local_ip, 27017)['scrapy2']['questions'].find()
    # local_user_profile = MongoClient(local_ip, 27017)['scrapy2']['user_profile'].find()

    remote_zhihu_user_data_ids = MongoClient(remote_ip, 27017)['scrapy2']['zhihu_user_data_ids']
    # remote_questions = MongoClient(remote_ip, 27017)['scrapy2']['questions']
    # remote_user_profile = MongoClient(remote_ip, 27017)['scrapy2']['user_profile']

    items_each = 20000
    total_time = local_zhihu_user_data_ids.count() / items_each
    for i in range(0, total_time):
        logging.log(logging.INFO, time.strftime(" %Y-%m-%d %H:%M:%S ") +
                    "fetching NO.%s" % i)
        try:
            remote_zhihu_user_data_ids.insert(local_zhihu_user_data_ids.find()
                                              .skip(items_each * i)
                                              .limit(items_each))
        except DuplicateKeyError:
            logging.log(logging.INFO, time.strftime(" %Y-%m-%d %H:%M:%S ") +
                        "dup")