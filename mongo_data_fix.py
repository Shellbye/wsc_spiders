__author__ = 'shellbye'
from pymongo import MongoClient

from wsc.settings import IP, DB

zhihu_user_data_ids = MongoClient(IP, 27017)[DB]['zhihu_user_data_ids']
user_profile = MongoClient(IP, 27017)[DB]['user_profile']


def process():
    count = 0
    data_ids = zhihu_user_data_ids.find({"fetched": True, "crawled_successfully": False}).sort([("_id", -1)])
    for data_id in data_ids:
        print count
        user_data_id = data_id['user_data_id']
        user = user_profile.find({"user_data_id": user_data_id})
        c = user.count()
        print c
        if c:
            print "pass..." + user_data_id
            pass
        else:
            print "delete." + user_data_id
            zhihu_user_data_ids.update({"user_data_id": user_data_id},
                                       {"$set": {"fetched": False}}
            )
        count += 1


if __name__ == "__main__":
    process()
    print "leaving"


# Or simply use the MongoDB shell command
#   `db.zhihu_user_data_ids.update({"crawled_successfully": false}, {$set:{"fetched": false}}, { multi: true })`