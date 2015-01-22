# -*- coding: utf-8 -*-
import scrapy


class ZhihuItem(scrapy.Item):
    count = scrapy.Field()


class ProxyTestSpider(scrapy.Spider):
    name = "proxy_test"
    allowed_domains = ["ip.chinaz.com"]
    start_urls = (
        'http://ip.chinaz.com/',
    )
    count = 0

    def parse(self, response):
        if 'proxy' in response.request.meta:
            print "meta proxy:" + response.request.meta['proxy']
        print response.xpath("//strong[@class='red']/text()")[0].extract()