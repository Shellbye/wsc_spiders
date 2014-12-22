# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from ..items import ZhiHuUserProfile


class UserProfileSpider(scrapy.Spider):
    name = "user_profile"
    allowed_domains = ["zhihu.com"]
    start_urls = (
        'http://www.zhihu.com/login',
        # 'http://www.zhihu.com/people/roc-lee-md',
        # 'http://www.zhihu.com/people/roc-lee-md/followers',
    )

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'email': 'jianguo.bai@hirebigdata.cn', 'password': 'wsc111111'},
            callback=self.login
        )

    def login(self, response):
        # 密码错误： "errcode": 270,
        # 邮箱尚未注册："errcode": 269,
        if 'errcode' in response.body:
            return
        else:
            # print response.body
            yield Request('http://www.zhihu.com/people/roc-lee-md/followers', callback=self.parse_follower)

    def parse_follower(self, response):
        followers = response.xpath("//div[@class='zm-profile-card zm-profile-section-item zg-clear no-hovercard']")
        for f in followers:
            id = f.xpath("descendant::div[@class='zg-right']/button/@data-id")[0].extract()
            print id
        return

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

    def parse_profile(self, response):
        id = response.xpath("//div[@class='zm-profile-header-op-btns clearfix']/button/@data-id")[0].extract()
        name = response.xpath("//span[@class='name']/text()")[0].extract()
        bio = response.xpath("//span[@class='bio']/text()")[0].extract()
        location = response.xpath("//span[contains(@class,'location')]/text()")[0].extract()
        business = response.xpath("//span[contains(@class,'business')]/a/text()")[0].extract()
        business_topic_url = "http://www." + self.allowed_domains[0] + \
                             response.xpath("//span[contains(@class,'business')]/a/@href")[0].extract()
        gender = response.xpath("//span[contains(@class,'gender')]/i/@class")[0].extract()
        # icon icon-profile-female
        # icon icon-profile-male
        employment = response.xpath("//span[contains(@class,'employment')]/text()")[0].extract()
        position = response.xpath("//span[contains(@class,'position')]/text()")[0].extract()
        description = response.xpath("//span[contains(@class,'description')]//span//text()")[0].extract().strip()
        agree_count = response.xpath("//span[@class='zm-profile-header-user-agree']//strong/text()")[0].extract()
        thanks_count = response.xpath("//span[@class='zm-profile-header-user-thanks']//strong/text()")[0].extract()
        item = ZhiHuUserProfile(id=id, name=name, bio=bio, location=location, business=business, business_topic_url=business_topic_url,
                                gender=gender, employment=employment, position=position, description=description,
                                agree_count=agree_count, thanks_count=thanks_count)
        return item