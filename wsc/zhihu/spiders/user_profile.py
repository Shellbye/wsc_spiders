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

    def __init__(self, user_data_id='114b18c0ed112db921e3c40fb689248f'):
        super(UserProfileSpider, self).__init__()
        self.user_data_id = user_data_id

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
            yield Request('http://www.zhihu.com/people/' + self.user_data_id,
                          callback=self.parse_profile)

    def parse_profile(self, response):
        item = ZhiHuUserProfile()
        item['questions'] = []
        item['answers'] = []
        item['locations'] = []
        item['employments'] = []
        item['educations'] = []
        user_url_name = response.url[28:]
        for attr in self.user_profile_fields.keys():
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
        profile_lists = response.xpath("//div[@class='zm-profile-module zg-clear']")
        user_item = response.meta['item']
        for profile_list in profile_lists:
            for key in self.user_profile_list_fields.keys():
                items = profile_list.xpath("descendant::ul[@class='zm-profile-details-items']/li")
                title = profile_list.xpath("descendant::h3/i/@class")[0].extract()
                if key != title:
                    continue
                for item in items:
                    text = item.xpath("@data-title")[0].extract()
                    sub = item.xpath("@data-sub-title")[0].extract()
                    if sub:
                        text += " - " + sub
                    user_item[self.user_profile_list_fields[key]].append(text)
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
            for attr in self.user_question_fields.keys():
                question_item[attr] = UserProfileSpider.get_detail(question, attr, 'user_question_fields')
            yield Request('http://www.zhihu.com' + question_item['question_id'],
                          callback=self.parse_question_tags,
                          meta={'item': response.meta['item'], 'question_item': question_item})

    def parse_question_tags(self, response):
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
            for attr in self.user_answer_fields.keys():
                answer_item[attr] = UserProfileSpider.get_detail(answer, attr, 'user_answer_fields')
            yield Request('http://www.zhihu.com' + answer_item['answer_id'],
                          meta={'item': response.meta['item'], 'answer_item': answer_item},
                          callback=self.parse_answer_content)

    def parse_answer_content(self, response):
        item = response.meta['item']
        answer_item = response.meta['answer_item']
        content = response.xpath("//div[@class=' zm-editable-content clearfix']")[0].extract()
        answer_item['answer_content'] = content
        item['answers'].append(answer_item)
        return item

    @staticmethod
    def get_detail(selector, attr, source, order=0, default=None):
        if source == 'user_profile_fields':
            fields = UserProfileSpider.user_profile_fields[attr]
        elif source == 'user_answer_fields':
            fields = UserProfileSpider.user_answer_fields[attr]
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
    user_profile_list_fields = {
        'zm-profile-icon zm-profile-icon-location': 'locations',
        'zm-profile-icon zm-profile-icon-company': 'employments',
        'zm-profile-icon zm-profile-icon-edu': 'educations',
    }
    user_answer_fields = {
        'answer_id': {
            'method': 'xpath',
            'params': "descendant::h2/a/@href",
        },
        'answer_title': {
            'method': 'xpath',
            'params': "descendant::h2/a/text()",
        },
        'answer_bio': {
            'method': 'xpath',
            'params': "descendant::h3[@class='zm-item-answer-author-wrap']/strong/@title",
        },
        'answer_vote_up': {
            'method': 'xpath',
            'params': "descendant::a[@class='zm-item-vote-count']/text()",
        },
        'answer_time': {
            'method': 'xpath',
            'params': "descendant::a[@class='answer-date-link meta-item']/text()",
        },
    }
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
        # 'location': {
        #     'method': 'xpath',
        #     'params': "//span[contains(@class,'location')]/text()",
        # },
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
        # 'employment': {
        #     'method': 'xpath',
        #     'params': "//span[contains(@class,'employment')]/text()",
        # },
        # 'position': {
        #     'method': 'xpath',
        #     'params': "//span[contains(@class,'position')]/text()",
        # },
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
        'followee_count': {
            'method': 'xpath',
            'params': "//div[@class='zm-profile-side-following zg-clear']/a[1]/strong/text()",
        },
        'follower_count': {
            'method': 'xpath',
            'params': "//div[@class='zm-profile-side-following zg-clear']/a[2]/strong/text()",
        },
        'questions_count': {
            'method': 'xpath',
            'params': "//div[@class='profile-navbar clearfix']/a[2]/span/text()",
        },
        'answers_count': {
            'method': 'xpath',
            'params': "//div[@class='profile-navbar clearfix']/a[3]/span/text()",
        },
        'posts_count': {
            'method': 'xpath',
            'params': "//div[@class='profile-navbar clearfix']/a[4]/span/text()",
        },
        'collections_count': {
            'method': 'xpath',
            'params': "//div[@class='profile-navbar clearfix']/a[5]/span/text()",
        },
        'logs_count': {
            'method': 'xpath',
            'params': "//div[@class='profile-navbar clearfix']/a[6]/span/text()",
        },
        'personal_page_view_count': {
            'method': 'xpath',
            'params': "//div[@class='zm-profile-side-section']/div[@class='zm-side-section-inner']/span/strong/text()",
        },
        'follow_columns_count': {
            'method': 'xpath',
            'params': "//a[contains(@href,'/columns/followed')]/strong/text()",
        },
        'follow_topics_count': {
            'method': 'xpath',
            'params': "//a[contains(@href,'/topics')]/strong/text()",
        },
    }
