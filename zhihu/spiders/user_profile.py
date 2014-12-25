# -*- coding: utf-8 -*-
from scrapy.http import Request
from scrapy import log
from scrapy import signals
from scrapy.selector import SelectorList
from scrapy.xlib.pydispatch import dispatcher

from zhihu.items import *
from fields_download import FieldsDownload


class UserProfileSpider(scrapy.Spider):
    name = "user_profile"
    collection = "user_profile"
    unique_key = 'user_data_id'
    allowed_domains = ["zhihu.com"]
    start_urls = (
        'http://www.zhihu.com/login',
    )

    def __init__(self, user_data_id='114b18c0ed112db921e3c40fb689248f'):
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
        user_url_name = response.url[28:]
        log.msg("user url name: " + user_url_name, level=log.INFO)
        for attr in FieldsDownload.user_profile_fields.keys():
            item[attr] = UserProfileSpider.get_detail(response, attr, 'user_profile_fields')
        yield Request("http://www.zhihu.com/people/" + user_url_name + "/about",
                      callback=self.parse_profile_list,
                      meta={
                          'item': item,
                      })
        yield Request("http://www.zhihu.com/people/" + user_url_name + "/asks",
                      callback=self.parse_questions,
                      meta={
                          'item': item,
                      })
        yield Request("http://www.zhihu.com/people/" + user_url_name + "/answers",
                      callback=self.parse_answers,
                      meta={
                          'item': item,
                      })

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

    def parse_follower(self, response):
        followers = response.xpath("//div[@class='zm-profile-card "
                                   "zm-profile-section-item zg-clear no-hovercard']")
        for f in followers:
            user_data_id = f.xpath("descendant::div[@class='zg-right']/button/@data-id")[0].extract()
            yield Request('http://www.zhihu.com/people/' + user_data_id, callback=self.parse_profile)

    def parse_followee(self, response):
        followees = response.xpath("//div[@class='zm-profile-card "
                                   "zm-profile-section-item zg-clear no-hovercard]")
        for f in followees:
            user_data_id = f.xpath("descendant::div[@class='zg-right']/button/@data-id")[0].extract()
            yield Request('http://www.zhihu.com/people/' + user_data_id, callback=self.parse_profile)

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
        content = response.xpath("//div[@class=' zm-editable-content clearfix']")[0].extract()
        answer_item['answer_content'] = content
        item['answers'].append(answer_item)
        return item

    @staticmethod
    def get_detail(selector, attr, source):
        fields = getattr(FieldsDownload, source)[attr]
        element = getattr(selector, fields['method'])(fields['params'])
        if 'process' in fields:
            element = getattr(UserProfileSpider, fields['process'])(element)
        if element and isinstance(element, SelectorList):
            return element[0].extract()
        else:
            return element

    @staticmethod
    def get_more_data():
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
                _xsrf的值在cookie中
                没有更多关注者msg为空
        input:
            _xsrf
        output:
            ids
        """
        pass

    @staticmethod
    def process_url_name(url_name):
        if not url_name:
            return None
        return url_name[28:]