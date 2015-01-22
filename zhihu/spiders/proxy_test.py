# -*- coding: utf-8 -*-
import scrapy


class ZhihuItem(scrapy.Item):
    count = scrapy.Field()


class ProxyTestSpider(scrapy.Spider):
    name = "proxy_test"
    allowed_domains = ["ip.cn"]
    start_urls = (
        'http://www.ip.cn/',
    )
    count = 0

    def parse(self, response):
        if 'proxy' in response.request.meta:
            print "meta proxy:" + response.request.meta['proxy']
        if response.xpath("//div[@id='result']/div/p/code/text()"):
            print response.xpath("//div[@id='result']/div/p/code/text()")[0].extract()
        else:
            print "list out of index"