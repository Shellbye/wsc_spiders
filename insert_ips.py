__author__ = 'shellbye'
from pymongo import MongoClient
from wsc.settings import IP, DB

zhihu_user_data_ids = MongoClient(IP, 27017)[DB]['zhihu_user_data_ids']
with open("zhihuUserRealIDs.txt", 'r') as f:
    count = 0
    for data_id in f:
        user = zhihu_user_data_ids.find_one({"user_data_id": data_id})
        if user:
            continue
        else:
            zhihu_user_data_ids.insert({"user_data_id": data_id.strip(),
                                        "crawled": False,
                                        "crawled_count": 0,
                                        "last_crawled_time": None})
            print "inserted: " + data_id
        count += 1
        print "current count: " + str(count)