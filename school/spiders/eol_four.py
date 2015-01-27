# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request


class EOLFourProfile(scrapy.Item):
    province = scrapy.Field()
    location = scrapy.Field()
    property = scrapy.Field()
    phone = scrapy.Field()
    zipcode = scrapy.Field()
    school_stage = scrapy.Field()
    address = scrapy.Field()
    website = scrapy.Field()


class EOLFourSpider(scrapy.Spider):
    name = "eol_four"
    collection = "eol_four"
    allowed_domains = ["xuexiao.eol.cn"]
    start_urls = (
        'http://xuexiao.eol.cn/',
    )

    def parse(self, response):
        pass