# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from ..items import ZhiHuUserProfile


class UserProfileSpider(scrapy.Spider):
    name = "user_profile"
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
            yield Request('http://www.zhihu.com/people/roc-lee-md/followers', callback=self.parse_follower)

    def parse_follower(self, response):
        followers = response.xpath("//div[@class='zm-profile-card zm-profile-section-item zg-clear no-hovercard']")
        for f in followers:
            user_data_id = f.xpath("descendant::div[@class='zg-right']/button/@data-id")[0].extract()
            yield Request('http://www.zhihu.com/people/' + user_data_id, callback=self.parse_profile)

    def parse_followee(self, response):
        followees = response.xpath("//div[@class='zm-profile-card zm-profile-section-item zg-clear no-hovercard]")
        for f in followees:
            user_data_id = f.xpath("descendant::div[@class='zg-right']/button/@data-id")[0].extract()
            yield Request('http://www.zhihu.com/people/' + user_data_id, callback=self.parse_profile)

    @staticmethod
    def get_profile_detail(selector, path, order=0, default=None):
        element = selector.xpath(path)
        if element:
            return element[order].extract()
        else:
            return default

    user_profile_fields = {
        'user_data_id': "//div[@class='zm-profile-header-op-btns clearfix']/button/@data-id",
        'name': "//div[@class='title-section ellipsis']/span[@class='name']/text()",
        'bio': "//span[@class='bio']/text()",
        'location': "//span[contains(@class,'location')]/text()",
        'business': "//span[contains(@class,'business')]/a/text()",
        'business_topic_url': "//span[contains(@class,'business')]/a/@href",
        'gender': "//span[contains(@class,'gender')]/i/@class",
        'employment': "//span[contains(@class,'employment')]/text()",
        'position': "//span[contains(@class,'position')]/text()",
        'description': "//span[contains(@class,'description')]//span//text()",
        'agree_count': "//span[@class='zm-profile-header-user-agree']//strong/text()",
        'thanks_count': "//span[@class='zm-profile-header-user-thanks']//strong/text()",
        'weibo_url': "//div[@class='weibo-wrap']/a/@href",
    }

    def parse_profile(self, response):
        # icon icon-profile-female
        # icon icon-profile-male
        item = ZhiHuUserProfile()
        for attr in ZhiHuUserProfile.fields.keys():
            item[attr] = UserProfileSpider.get_profile_detail(response, self.user_profile_fields[attr])
        return item

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