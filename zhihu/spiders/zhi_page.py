# -*- coding: utf-8 -*-
import scrapy
from scrapy import log
from scrapy import Request
from scrapy import FormRequest


class ZhiPageSpider(scrapy.Spider):
    name = "zhi_page"
    allowed_domains = ["zhihu.com"]
    start_urls = (
        'http://www.zhihu.com/',
    )

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
            yield Request('http://www.zhihu.com/people/chengyuan/followees',
                          callback=self.parse_page)

    def parse_page(self, response):
        _xsrf = str(response.xpath("//input[@name='_xsrf']/@value")[0].extract())
        url = 'http://www.zhihu.com/node/ProfileFolloweesListV2'
        offset = 20
        params = {
            "offset": offset,
            "order_by": "created",
            "hash_id": '1166f0aae6dfccf3d89ad6e065804593'
        }

        post_params = {"params": params, "method": "next", "_xsrf": _xsrf}
        print post_params
        yield FormRequest(url=url, formdata=post_params, callback=self.parse_final)

    def parse_final(self, response):
        print response