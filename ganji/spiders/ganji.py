# -*- coding: utf-8 -*-
import time
import scrapy


class GanjiItem(scrapy.Item):
    url = scrapy.Field()  # url√
    city = scrapy.Field()  # 城市√
    name = scrapy.Field()  # 公司名√
    size = scrapy.Field()  # 公司规模√
    trade = scrapy.Field()  # 公司行业√
    type = scrapy.Field()  # 公司类型√
    benefits = scrapy.Field()  # 公司福利√
    homepage = scrapy.Field()  # 公司网址√
    phonenumber = scrapy.Field()  # 联系方式√
    contacts = scrapy.Field()  # 联系人√
    address = scrapy.Field()  # 公司地址√
    # mail = scrapy.Field()  # 公司邮箱√
    brief = scrapy.Field()  # 公司简介√
    license = scrapy.Field()  # 执照名称√
    jd = scrapy.Field()  # 招聘职位
    # job_url
    # job_title
    # job_name
    # job_salary
    # job_number
    # job_education
    # job_experience
    # job_age
    # job_place
    # job_phone
    # job_contacts
    crawled_time = scrapy.Field()

bigger_that_max_page = 1000


class GanjiSpider(scrapy.Spider):
    name = "ganji"
    collection = "ganji_gongsi"
    allowed_domains = ["ganji.com"]
    start_urls = (
        'http://www.ganji.com/index.htm?goto=gongsi',
    )

    def parse(self, response):
        for e in response.xpath('//div[@class="all-city"]//a'):
            city = e.xpath('text()')[0].extract()
            city_url = e.xpath('@href')[0].extract()
            yield scrapy.Request(city_url + 'gongsi/o' + str(bigger_that_max_page) + '/',
                                 callback=self.parse_city_page,
                                 meta={'city': city, 'city_url': city_url})

    def parse_city_page(self, response):
        page_count = response.xpath("//a[@class='c linkOn']/span/text()")[0].extract()
        city = response.meta['city']
        city_url = response.meta['city_url']
        for i in range(1, page_count):
            yield scrapy.Request(city_url + 'gongsi/o' + str(i) + '/',
                                 callback=self.parse_city_companies,
                                 meta={'city': city, 'city_url': city_url})

    def parse_city_companies(self, response):
        item = GanjiItem()
        item['url'] = response.url
        item['city'] = response.meta['city']
        item['name'] = response.meta['name']
        item['crawled_time'] = time.strftime("%Y-%m-%d:%H:%M:%S")
        item['license'] = ""
        item['size'] = ""
        item['trade'] = ""
        item['type'] = ""
        item['contacts'] = ""
        item['phonenumber'] = ""
        item['address'] = ""
        item['homepage'] = ""
        item['brief'] = response.xpath("//div[@class='c-introduce']/p")[0].extract()
        item['benefits'] = []
        for a in response.xpath("//div[@class='d-c-left-ico']//dd"):
            item['benefits'].add(a.xpath("span/text()")[0].extract())
        item['jd'] = []
        all_li = response.xpath("//div[@class='c-introduce']/ul/li")
        for li in all_li:
            key = li.xpath("em/text()")[0].extract()
            if key == u'公司名称：':
                pass
            if key == u'公司网站：':
                item['homepage'] = li.xpath("text()")[0].extract()
            if key == u'执照名称：':
                item['license'] = li.xpath("text()")[0].extract()
            if key == u'公司规模：':
                item['size'] = li.xpath("text()")[0].extract()
            if key == u'公司行业：':
                item['trade'] = li.xpath("a/text()")[0].extract()
            if key == u'公司类型：':
                item['type'] = li.xpath("a/text()")[0].extract()
            if key == u'联系人：':
                item['contacts'] = li.xpath("text()")[0].extract()
            if key == u'联系电话：':
                item['phonenumber'] = "www.ganji.com" + li.xpath("img/@src")[0].extract()
            if key == u'公司地址：':
                item['address'] = li.xpath("text()")[0].extract()
        return item
