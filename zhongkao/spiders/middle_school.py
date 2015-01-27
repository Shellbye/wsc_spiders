# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request


class MiddleSchoolProfile(scrapy.Item):
    url = scrapy.Field()
    province = scrapy.Field()
    school_stage = scrapy.Field()
    school_type = scrapy.Field()
    full_name = scrapy.Field()
    class_type = scrapy.Field()
    headmaster = scrapy.Field()
    accommodation = scrapy.Field()
    build_time = scrapy.Field()
    enrol_method = scrapy.Field()
    phone = scrapy.Field()
    test_type = scrapy.Field()
    address = scrapy.Field()
    special_enrol = scrapy.Field()
    website = scrapy.Field()


class MiddleSchoolSpider(scrapy.Spider):
    name = "middle_school"
    collection = "middle_school"
    unique_key = 'url'
    allowed_domains = ["school.aoshu.com"]
    start_urls = (
        'http://school.aoshu.com/province/',
    )

    def parse(self, response):
        total_page = int(response.xpath("//nav[@class='page_Box tc']/a[10]/text()")[0].extract())
        for i in range(1, total_page + 1):
            link = "http://school.aoshu.com/province/0/p" + str(i)
            yield Request(link, callback=self.parse_2)

    def parse_2(self, response):
        for s in response.xpath("//article[@class='filtschinfo clearfix']"):
            link = s.xpath("descendant::a[1]/@href")[0].extract()
            yield Request(link, callback=self.parse_3)

    def parse_3(self, response):
        school_intro = response.xpath("//article[@class='schoolintro']")
        h = MiddleSchoolProfile()
        h['url'] = response.url
        h['province'] = response.xpath("//nav[@class='wrapper tm10']/a[2]/text()")[0].extract()
        h['school_stage'] = 'middle_school'
        h['school_type'] = school_intro.xpath("descendant::table/tr[1]/td[1]/text()")[0].extract()
        h['full_name'] = school_intro.xpath("descendant::table/tr[1]/td[2]/a/text()")[0].extract()
        h['class_type'] = school_intro.xpath("descendant::table/tr[2]/td[1]/text()")[0].extract()
        h['headmaster'] = school_intro.xpath("descendant::table/tr[2]/td[2]/text()")[0].extract()
        h['accommodation'] = school_intro.xpath("descendant::table/tr[3]/td[1]/text()")[0].extract()
        h['build_time'] = school_intro.xpath("descendant::table/tr[3]/td[2]/text()")[0].extract()
        h['enrol_method'] = school_intro.xpath("descendant::table/tr[4]/td[1]/text()")[0].extract()
        h['phone'] = school_intro.xpath("descendant::table/tr[4]/td[2]/text()")[0].extract()
        h['test_type'] = school_intro.xpath("descendant::table/tr[5]/td[1]/text()")[0].extract()
        h['address'] = school_intro.xpath("descendant::table/tr[5]/td[2]/text()")[0].extract()
        h['special_enrol'] = school_intro.xpath("descendant::table/tr[6]/td[1]/text()")[0].extract()
        h['website'] = school_intro.xpath("descendant::table/tr[6]/td[2]/text()")[0].extract()
        return h