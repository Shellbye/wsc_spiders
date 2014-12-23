# -*- coding: utf-8 -*-
from scrapy.http import Request
from ..items import *


class UserProfileSpider(scrapy.Spider):
    name = "user_profile"
    collection = "user_profile"
    unique_key = 'user_data_id'
    allowed_domains = ["zhihu.com"]
    start_urls = (
        'http://www.zhihu.com/login',
    )

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'email': 'jianguo.bai@hirebigdata.cn', 'password': 'wsc111111'},
            callback=self.login
        )

    def login(self, response):
        if 'errcode' in response.body:
            return
        else:
            yield Request('http://www.zhihu.com/people/roc-lee-md',
                          callback=self.parse_profile)

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

    def parse_ask(self, response):
        item = response.meta['item']
        questions = response.xpath("//div[@class='zm-profile-section-item zg-clear']")
        questions_list = []
        for question in questions:
            question_item = {}
            for attr in self.user_question_fields.keys():
                question_item[attr] = UserProfileSpider.get_detail(question, attr, 'user_question_fields')
            questions_list.append(question_item)
        item['questions'] = questions_list
        return item

    def parse_answers(self, response):
        pass

    @staticmethod
    def get_detail(selector, attr, source, order=0, default=None):
        if source == 'user_profile_fields':
            fields = UserProfileSpider.user_profile_fields[attr]
        else:
            fields = UserProfileSpider.user_question_fields[attr]
        method = fields['method']
        if method == 'xpath':
            path = fields['params']
            element = selector.xpath(path)
            if element:
                return element[order].extract()
            else:
                return default
        elif method == 'attribute':
            return getattr(selector, fields['params'])
        else:
            return None

    user_question_fields = {
        'question_id': {
            'method': 'xpath',
            'params': "descendant::a[@class='question_link']/@href",
        },
        'question_title': {
            'method': 'xpath',
            'params': "descendant::a[@class='question_link']/text()",
        },
        'question_answer_count': {
            'method': 'xpath',
            'params': "descendant::div[@class='meta zg-gray']/span[1]/following-sibling::text()",
        },
        'question_follower_count': {
            'method': 'xpath',
            'params': "descendant::div[@class='meta zg-gray']/span[2]/following-sibling::text()",
        },
        'question_view_count': {
            'method': 'xpath',
            'params': "descendant::div[@class='zm-profile-vote-num']/text()",
        },
    }

    user_profile_fields = {
        'user_data_id': {
            'method': 'xpath',
            'params': "//div[@class='zm-profile-header-op-btns clearfix']/button/@data-id",
        },
        'name': {
            'method': 'xpath',
            'params': "//div[@class='title-section ellipsis']/span[@class='name']/text()",
        },
        'url_name': {
            'method': 'attribute',
            'params': 'url'
        },
        'bio': {
            'method': 'xpath',
            'params': "//span[@class='bio']/text()",
        },
        'location': {
            'method': 'xpath',
            'params': "//span[contains(@class,'location')]/text()",
        },
        'business': {
            'method': 'xpath',
            'params': "//span[contains(@class,'business')]/a/text()",
        },
        'business_topic_url': {
            'method': 'xpath',
            'params': "//span[contains(@class,'business')]/a/@href",
        },
        'gender': {
            'method': 'xpath',
            'params': "//span[contains(@class,'gender')]/i/@class",
        },
        'employment': {
            'method': 'xpath',
            'params': "//span[contains(@class,'employment')]/text()",
        },
        'position': {
            'method': 'xpath',
            'params': "//span[contains(@class,'position')]/text()",
        },
        'description': {
            'method': 'xpath',
            'params': "//span[contains(@class,'description')]//span//text()",
        },
        'agree_count': {
            'method': 'xpath',
            'params': "//span[@class='zm-profile-header-user-agree']//strong/text()",
        },
        'thanks_count': {
            'method': 'xpath',
            'params': "//span[@class='zm-profile-header-user-thanks']//strong/text()",
        },
        'weibo_url': {
            'method': 'xpath',
            'params': "//div[@class='weibo-wrap']/a/@href",
        },
    }

    def parse_profile(self, response):
        item = ZhiHuUserProfile()
        for attr in self.user_profile_fields.keys():
            item[attr] = UserProfileSpider.get_detail(response, attr, 'user_profile_fields')
        yield Request("http://www.zhihu.com/people/roc-lee-md/asks",
                      callback=self.parse_ask,
                      meta={
                          'item': item,
                      })

    @staticmethod
    def get_more_followers():
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
    def extract_data(data):
        return data[0].extract()