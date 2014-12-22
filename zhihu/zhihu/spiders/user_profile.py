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
            user_data_id = f.xpath("descendant::div[@class='zg-right']/button/@data-id")[0].extract()
            print user_data_id
            yield Request('http://www.zhihu.com/people/' + user_data_id, callback=self.parse_profile)

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
        user_data_id_selector = response.xpath("//div[@class='zm-profile-header-op-btns clearfix']/button/@data-id")
        if user_data_id_selector:
            user_data_id = user_data_id_selector[0].extract()
        else:
            user_data_id = None
        name_selector = response.xpath("//div[@class='title-section ellipsis']/span[@class='name']/text()")
        if name_selector:
            name = name_selector[0].extract()
        else:
            name = None
        bio_selector = response.xpath("//span[@class='bio']/text()")
        if bio_selector:
            bio = bio_selector[0].extract()
        else:
            bio = None
        location_selector = response.xpath("//span[contains(@class,'location')]/text()")
        if location_selector:
            location = location_selector[0].extract()
        else:
            location = None
        business_selector = response.xpath("//span[contains(@class,'business')]/a/text()")
        if business_selector:
            business = business_selector[0].extract()
        else:
            business = None
        business_topic_url_selector = response.xpath("//span[contains(@class,'business')]/a/@href")
        if business_topic_url_selector:
            business_topic_url = business_topic_url_selector[0].extract()
        else:
            business_topic_url = None
        gender_selector = response.xpath("//span[contains(@class,'gender')]/i/@class")
        if gender_selector:
            gender = gender_selector[0].extract()
        # icon icon-profile-female
        # icon icon-profile-male
        else:
            gender = None
        employment_selector = response.xpath("//span[contains(@class,'employment')]/text()")
        if employment_selector:
            employment = employment_selector[0].extract()
        else:
            employment = None
        position_selector = response.xpath("//span[contains(@class,'position')]/text()")
        if position_selector:
            position = position_selector[0].extract()
        else:
            position = None
        description_selector = response.xpath("//span[contains(@class,'description')]//span//text()")
        if description_selector:
            description = description_selector[0].extract().strip()
        else:
            description = None
        agree_count_selector = response.xpath("//span[@class='zm-profile-header-user-agree']//strong/text()")
        if agree_count_selector:
            agree_count = agree_count_selector[0].extract()
        else:
            agree_count = None
        thanks_count_selector = response.xpath("//span[@class='zm-profile-header-user-thanks']//strong/text()")
        if thanks_count_selector:
            thanks_count = thanks_count_selector[0].extract()
        else:
            thanks_count = None
        print name
        item = ZhiHuUserProfile(user_data_id=user_data_id, name=name, bio=bio, location=location, business=business, business_topic_url=business_topic_url,
                                gender=gender, employment=employment, position=position, description=description,
                                agree_count=agree_count, thanks_count=thanks_count)
        return item