# -*- coding: utf-8 -*-
import time
import math
import urllib
import urllib2

from scrapy.http import Request
from scrapy import log
from scrapy import signals
from scrapy.selector import SelectorList, Selector
from scrapy.xlib.pydispatch import dispatcher
from pymongo import MongoClient

from zhihu.items import *
from fields_download import FieldsDownload
from wsc.settings import IP, DB, DEBUG


class UserProfileSpider(scrapy.Spider):
    name = "user_profile"
    if DEBUG:
        collection = "user_profile_debug"
    else:
        collection = "user_profile"
    zhihu_user_data_ids = MongoClient(IP, 27017)[DB]['zhihu_user_data_ids']
    unique_key = 'user_data_id'
    allowed_domains = ["zhihu.com"]
    start_urls = (
        'http://www.zhihu.com/login',
    )

    def __init__(self, user_data_id='18c79c6cc76ce8db8518367b46353a54'):
        super(UserProfileSpider, self).__init__()
        dispatcher.connect(self.closed, signals.spider_closed)
        self.user_data_id = user_data_id
        log.msg("start crawl " + user_data_id, level=log.INFO)

    def closed(self, spider):
        if spider is not self:
            return
        log.msg("crawl ended", level=log.INFO)

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'email': 'jianguo.bai@hirebigdata.cn', 'password': 'wsc111111'},
            callback=self.login
        )

    def login(self, response):
        if 'errcode' in response.body:
            log.msg("login error: " + response.body, level=log.ERROR)
            return
        else:
            log.msg("login successfully", level=log.INFO)
            yield Request('http://www.zhihu.com/people/' + self.user_data_id,
                          callback=self.parse_profile)

    def parse_profile(self, response):
        if response.status == 404:
            log.msg("user not exist: " + response.url[28:], level=log.ERROR)
        item = ZhiHuUserProfile()
        item['questions'] = []
        item['answers'] = []
        item['locations'] = []
        item['employments'] = []
        item['educations'] = []
        item['columns'] = []
        item['topics'] = []
        item['skilled_topics'] = []
        user_url_name = response.url[28:]
        log.msg("user url name: " + user_url_name, level=log.INFO)
        for attr in FieldsDownload.user_profile_fields.keys():
            item[attr] = UserProfileSpider.get_detail(response, attr, 'user_profile_fields')
        skilled_topics = response.xpath("//div[@class='zm-profile-section-wrap skilled-topics']"
                                        "/div[@class='inner zg-clear']"
                                        "/div[@class='zm-profile-section-list zg-clear']"
                                        "/div[@class='item']")
        for st in skilled_topics:
            t = {
                'name': st.xpath("descendant::div[@class='content']/div[@class='content-inner']/"
                                 "h3/text()")[0].extract(),
                'url': st.xpath("@data-url-token")[0].extract(),
                'vote': st.xpath("descendant::div[@class='content']/div[@class='content-inner']/"
                                 "p[@class='meta']/span/i[@class='zg-icon vote']/"
                                 "following-sibling::text()")[0].extract(),
                'comment': st.xpath("descendant::div[@class='content']/div[@class='content-inner']/"
                                    "p[@class='meta']/span/i[@class='zg-icon comment']/"
                                    "following-sibling::text()")[0].extract()
            }
            item['skilled_topics'].append(t)

        yield Request("http://www.zhihu.com/people/" + user_url_name + "/about",
                      callback=self.parse_profile_list,
                      meta={
                          'item': item,
                      })
        question_page = math.ceil(float(item['questions_count']) / 20.0)
        for page in range(1, int(question_page) + 1):
            yield Request("http://www.zhihu.com/people/" + user_url_name + "/asks?page=" + str(page),
                          callback=self.parse_questions,
                          meta={
                              'item': item,
                          })

        answer_page = math.ceil(float(item['answers_count']) / 20.0)
        for page in range(1, int(answer_page) + 1):
            yield Request("http://www.zhihu.com/people/" + user_url_name + "/answers?page=" + str(page),
                          callback=self.parse_answers,
                          meta={
                              'item': item,
                          })
        yield Request("http://www.zhihu.com/people/" + user_url_name + "/columns/followed",
                      callback=self.parse_followed_columns,
                      meta={
                          'item': item,
                      })
        yield Request("http://www.zhihu.com/people/" + user_url_name + "/topics",
                      callback=self.parse_followed_topics,
                      meta={
                          'item': item,
                      })
        yield Request("http://www.zhihu.com/people/" + user_url_name + "/followees",
                      callback=self.collect_followee,
                      meta={
                          'item': item,
                      })
        yield Request("http://www.zhihu.com/people/" + user_url_name + "/followers",
                      callback=self.collect_follower,
                      meta={
                          'item': item,
                      })
        user = UserProfileSpider.zhihu_user_data_ids.find_one({'user_data_id': self.user_data_id})
        if user:
            UserProfileSpider.zhihu_user_data_ids.update(user, {"$set": {"crawled_successfully": True}})

    def parse_followed_columns(self, response):
        user_item = response.meta['item']
        all_columns = response.xpath("//div[@class='zm-profile-section-item zg-clear']")
        for column in all_columns:
            column_item = {
                'url': column.xpath("descendant::a[@class='zm-list-avatar-link']/@href")[0].extract(),
                'name': column.xpath("descendant::div[@class='zm-profile-section-main']/a/strong/text()")[0].extract(),
                'description': column.xpath("descendant::div[@class='description']")[0].extract(),
                'meta': column.xpath("descendant::div[@class='meta']")[0].extract(),
            }
            user_item['columns'].append(column_item)
        return user_item

    def parse_followed_topics(self, response):
        user_item = response.meta['item']
        all_topics = response.xpath("//div[@class='zm-profile-section-item zg-clear']")
        for topic in all_topics:
            topic_item = {
                'url': topic.xpath("descendant::a[@class='zm-list-avatar-link']/@href")[0].extract(),
                'name': topic.xpath("descendant::div[@class='zm-profile-section-main']/a[2]/strong/text()")[0].extract(),
                'content': topic.xpath("descendant::div[@class='zm-editable-content']")[0].extract(),
                'answers_count': topic.xpath("descendant::a[@class='zg-link-gray']/text()")[0].extract(),
            }
            user_item['topics'].append(topic_item)
        return user_item

    def parse_profile_list(self, response):
        user_item = response.meta['item']
        profile_lists = response.xpath("//div[@class='zm-profile-module zg-clear']")
        for attr in FieldsDownload.user_reputation_fields.keys():
            user_item[attr] = UserProfileSpider.get_detail(response, attr, 'user_reputation_fields')
        for profile_list in profile_lists:
            for key in FieldsDownload.user_profile_list_fields.keys():
                items = profile_list.xpath("descendant::ul[@class='zm-profile-details-items']/li")
                title = profile_list.xpath("descendant::h3/i/@class")[0].extract()
                if key != title:
                    continue
                for item in items:
                    text = item.xpath("@data-title")[0].extract()
                    sub = item.xpath("@data-sub-title")[0].extract()
                    if sub:
                        text += " - " + sub
                    user_item[FieldsDownload.user_profile_list_fields[key]].append(text)
        return user_item

    def collect_follower(self, response):
        user_item = response.meta['item']
        followers = response.xpath("//div[@class='zm-profile-card "
                                   "zm-profile-section-item zg-clear no-hovercard']")
        followers_data_ids = []
        for f in followers:
            user_data_id = f.xpath("descendant::div[@class='zg-right']/button/@data-id")[0].extract()
            UserProfileSpider.insert_new_or_update_user_data_id(user_data_id)
            followers_data_ids.append(user_data_id)
        user_item['followers'] = followers_data_ids
        return user_item

    def collect_followee(self, response):
        user_item = response.meta['item']
        followees = response.xpath("//div[@class='zm-profile-card "
                                   "zm-profile-section-item zg-clear no-hovercard']")
        followees_data_ids = []
        for f in followees:
            user_data_id = f.xpath("descendant::div[@class='zg-right']/button/@data-id")[0].extract()
            UserProfileSpider.insert_new_or_update_user_data_id(user_data_id)
            followees_data_ids.append(user_data_id)
        user_item['followees'] = followees_data_ids
        return user_item

    def parse_questions(self, response):
        questions = response.xpath("//div[@class='zm-profile-section-item zg-clear']")
        for question in questions:
            question_item = {}
            for attr in FieldsDownload.user_question_fields.keys():
                question_item[attr] = UserProfileSpider.get_detail(question, attr, 'user_question_fields')
            yield Request('http://www.zhihu.com' + question_item['question_id'],
                          callback=self.parse_question_tags,
                          meta={'item': response.meta['item'], 'question_item': question_item})

    @staticmethod
    def parse_question_tags(response):
        item = response.meta['item']
        question_item = response.meta['question_item']
        tags = response.xpath("//div[@class='zm-tag-editor-labels zg-clear']/a/text()")
        ret = []
        for tag in tags:
            ret.append(tag.extract())
        question_item['tags'] = ret
        item['questions'].append(question_item)
        return item

    def parse_answers(self, response):
        answers = response.xpath("//div[@class='zm-item']")
        for answer in answers:
            answer_item = {}
            for attr in FieldsDownload.user_answer_fields.keys():
                answer_item[attr] = UserProfileSpider.get_detail(answer, attr, 'user_answer_fields')
            yield Request('http://www.zhihu.com' + answer_item['answer_id'],
                          meta={'item': response.meta['item'], 'answer_item': answer_item},
                          callback=self.parse_answer_content)

    @staticmethod
    def parse_answer_content(response):
        item = response.meta['item']
        answer_item = response.meta['answer_item']
        content = response.xpath("//div[@class=' zm-editable-content clearfix']")
        if content:
            content = content[0].extract()
        else:
            content = None
        answer_item['answer_content'] = content
        tags = response.xpath("//div[@class='zm-tag-editor-labels zg-clear']/a/text()")
        ret = []
        for tag in tags:
            ret.append(tag.extract())
        answer_item['answer_tags'] = ret
        item['answers'].append(answer_item)
        return item

    @staticmethod
    def get_detail(selector, attr, source):
        fields = getattr(FieldsDownload, source)[attr]
        element = getattr(selector, fields['method'])(fields['params'])
        if not element:
            return fields['default']
        if 'process' in fields:
            element = getattr(UserProfileSpider, fields['process'])(element)
        if element and isinstance(element, SelectorList):
            return element[0].extract()
        else:
            return element

    @staticmethod
    def insert_new_or_update_user_data_id(user_data_id):
        user = UserProfileSpider.zhihu_user_data_ids.find_one({'user_data_id': user_data_id})
        if not user:
            UserProfileSpider.zhihu_user_data_ids.insert({'user_data_id': user_data_id,
                                        "fetched": False,
                                        "crawled_successfully": False,
                                        "crawled_count": 1,
                                        "last_crawled_time": time.strftime("%Y-%m-%d:%H:%M:%S")})
        else:
            crawled_count = user['crawled_count'] + 1
            UserProfileSpider.zhihu_user_data_ids.update(
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

    @staticmethod
    def user_need_to_crawl(user_data_id):
        return UserProfileSpider.zhihu_user_data_ids.find_one({'user_data_id': user_data_id, "fetched": False})

    @staticmethod
    def get_more_columns(user_data_id, _xsrf, offset=20):
        # todo
        """
        data-access-method:
            url:
                http://www.zhihu.com/node/ProfileFollowersListV2
            input:
                method:next
                params:{"offset":80,"order_by":"created","hash_id":"114b18c0ed112db921e3c40fb689248f"}
                _xsrf:f1460d2580fbf34ccd508eb4489f1097
            output:
                {"r":0,"msg":[div_data...]}
            notice:
                _xsrf的值在cookie中和一个hidden的input中都有
                params中的hash_id就是用户的user_data_id
                没有更多关注者msg为空
        input:
            _xsrf
        output:
            ids
        UserProfileSpider.get_more_columns("18c79c6cc76ce8db8518367b46353a54", "d052a24539255e20ec4ef23de30d4e8e")
        """
        params = '{"offset": ' + str(offset) + ', "order_by": "created", "hash_id": ' + user_data_id + '}'
        post_params = urllib.urlencode({"params": params, "method": "next", "_xsrf": _xsrf})
        ret = urllib2.urlopen("http://www.zhihu.com/node/ProfileFollowersListV2", post_params)
        print ret

    @staticmethod
    def process_url_name(url_name):
        if not url_name:
            return None
        return url_name[28:]

    @staticmethod
    def process_questions_count(questions_count):
        if not questions_count:
            return 0
        return questions_count

    @staticmethod
    def process_selector_extract(selector):
        return selector.extract()[0]