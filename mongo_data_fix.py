__author__ = 'shellbye'
from pymongo import MongoClient

from wsc.settings import IP, DB

zhihu_user_data_ids = MongoClient(IP, 27017)[DB]['zhihu_user_data_ids']
user_profile = MongoClient(IP, 27017)[DB]['user_profile']
data_ids = zhihu_user_data_ids.find({"fetched": True}).sort([("$natural", -1)])
# print data_ids.count()
count = 0
for data_id in data_ids:
    # print data_id['user_data_id']
    # if count > 5:
    #     break
    user_data_id = data_id['user_data_id']
    user = user_profile.find({"user_data_id": user_data_id})
    c = user.count()
    # print c
    if c:
        # print "pass..." + user_data_id
        pass
    else:
        # print "delete." + user_data_id
        zhihu_user_data_ids.update(data_id,
                                   {
                                       "$set":
                                           {
                                               "fetched": False
                                           }
                                   }
        )
    # count += 1