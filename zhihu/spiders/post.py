# -*- coding: utf-8 -*-
import scrapy
import urllib
import json
from scrapy.http import Request, FormRequest


class PostSpider(scrapy.Spider):
    name = "post"
    allowed_domains = ["zhihu.com"]
    start_urls = (
        'http://www.zhihu.com',
    )

    def __init__(self):
        super(PostSpider, self).__init__()

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'email': 'jianguo.bai@hirebigdata.cn', 'password': 'wsc111111'},
            callback=self.login,
        )

    def login(self, response):
        print response.request.headers['Cookie']
        print response.request.headers
        print "login"
        params = {"offset": "20", "limit": "20", "hash_id": "18c79c6cc76ce8db8518367b46353a54"}
        method = 'next'
        _xsrf = 'f1460d2580fbf34ccd508eb4489f1097'
        data = {
            'params': params,
            'method': method,
            '_xsrf': _xsrf,
        }
        r = Request(
            "http://www.zhihu.com/node/ProfileFollowedColumnsListV2",
            method='POST',
            body=urllib.urlencode(data),
            headers={
                'Accept': '*/*',
                'Accept-Encoding': 'gzip,deflate',
                'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Cache-Control': 'no-cache',
                'Cookie': '_xsrf=f1460d2580fbf34ccd508eb4489f1097; '
                          'c_c=2a45b1cc8f3311e4bc0e52540a3121f7; '
                          '__utma=51854390.1575195116.1419486667.1419855627.1419902703.10; '
                          '__utmb=51854390.2.10.1419902703; '
                          '__utmc=51854390; '
                          '__utmz=51854390.1419855627.9.8.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/;'
                          '__utmv=51854390.100--|2=registration_date=20141222=1^3=entry_date=20141015=1;',
                'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Ubuntu Chromium/37.0.2062.120 Chrome/37.0.2062.120 Safari/537.36',
                'host': 'www.zhihu.com',
                'Origin': 'http://www.zhihu.com',
                'Referer': 'http://www.zhihu.com/people/hynuza/columns/followed',
                'Connection': 'keep-alive',
                'X-Requested-With': 'XMLHttpRequest',
            },
            callback=self.parse2)
        r.headers['Cookie'] += response.request.headers['Cookie']
        print r.headers
        yield r
        print "after"

    def parse2(self, response):
        print response.url
        followers = response.xpath("//div[@class='zm-profile-card "
                                   "zm-profile-section-item zg-clear no-hovercard']")
        print len(followers)


