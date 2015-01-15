# -*- coding:utf-8 -*-
import time
import re

import scrapy
from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request
from scrapy import log

from ..items import KanZhunItem
from ..items import JobItem


class KanzhunSpider(CrawlSpider):

    name = "kanzhun"
    collection = "kanzhun"

    allowed_domains = ["kanzhun.com"]
    start_urls = [
        "http://www.kanzhun.com/login/?ka=head-signin"
    ]

    def parse(self, response):
        return scrapy.FormRequest.from_response(response, formdata={'account': 'example@qq.com',
                                                                    'password': 'example'},
                                                callback=self.parse_all_company)

    def parse_all_company(self, response):
        if "authentication failed" in response.body:
            self.log("Login failed", level=log.ERROR)
            return
        else:
            for page in range(46, 51):                   #爬哪几页的公司
                yield Request(url="http://www.kanzhun.com/plc4p%d.html?ka=paging%d" % (page, page),
                              callback=self.parse_single_company)

    def parse_single_company(self, response):
        section = response.xpath('//section[@class="l_con clearfix"]')
        ul = section.xpath('descendant::ul[2]')
        li = ul.xpath('descendant::li')
        for i in range(0, 10):                   #爬单页多少个公司
            url = li[i].xpath('descendant::a')[0].xpath("@href")[0].extract()
            yield Request("http://www.kanzhun.com"+url, callback=self.parse_conpany_page)

    def parse_conpany_page(self, response):
        item = KanZhunItem()
        if response.xpath('//p[@id="companyName"]//text()').extract():
            item['name'] = response.xpath('//p[@id="companyName"]//text()').extract()[0]
        if response.xpath('//p[@class="msg"]//strong/text()').extract():
            item['score'] = response.xpath('//p[@class="msg"]//strong/text()').extract()[0]
        if len(response.xpath('//a[@class="grey_99"]/text()').extract()) > 1:
            item['url'] = response.xpath('//a[@class="grey_99"]/text()').extract()[1]
        if response.xpath('//a[@ka="com-industry"]/text()').extract():
            item['industry'] = response.xpath('//a[@ka="com-industry"]/text()').extract()[0]
        if response.xpath('//a[@ka="com-city"]/text()').extract():
            item['address'] = response.xpath('//a[@ka="com-city"]/text()').extract()[0]
        if response.xpath('//span[@class="def"]/text()').extract():
            item['scale'] = response.xpath('//span[@class="def"]/text()').extract()[0]
        if len(response.xpath('//span[@class="def"]/text()').extract()) > 1:
            item['ceo'] = response.xpath('//span[@class="def"]/text()').extract()[1]
        if response.xpath('//div[@class="competitors"]//a[@target="_blank"]//text()').extract():
            item['competitors'] = response.xpath('//div[@class="competitors"]//a[@target="_blank"]//text()').extract()[0]
        ul = response.xpath('//ul[@class="listed_detail mb20"]')
        if ul:
            li = ul.xpath('descendant::li')
            item['stockName'] = li[0].xpath('descendant::p/text()').extract()[0]
            item['stockCode'] = li[1].xpath('text()').extract()[0]
            item['stockLocation'] = li[2].xpath('text()').extract()[0]
            item['stockValue'] = li[3].xpath('descendant::em/text()').extract()[0]+li[3].xpath('text()').extract()[0]
        if len(response.xpath('//p//em[@class="def"]//text()').extract()) > 1:
            a = response.xpath('//p//em[@class="def"]//text()').extract()[1]
            p = re.compile(r'\d+')
            if len(p.findall(a)) > 1:
                job_number = p.findall(a)[1]
                job_url = response.xpath('//p//a[@ka="blocker4-seeall"]//@href').extract()[0]
                job_use = p.findall(job_url)[0]
                if int(job_number) % 10 != 0:
                    job_length = int(job_number)/10 + 2
                else:
                    job_length = int(job_number)/10 + 1
                for i in range(1, job_length):
                    url = "http://www.kanzhun.com/gsx%dp%d.html" % (int(job_use), i)
                    yield Request(url, callback=self.parse_page)
        yield item

    def parse_page(self, response):
        time.sleep(10)
        tr = response.xpath('//table[@id="salaryDescTable"]//tr')
        for i in range(1, len(tr), 2):
            k = i/2 + 1
            items = JobItem()
            items['name'] = response.xpath('//p[@id="companyName"]//text()').extract()[0]
            items['job'] = response.xpath('//a[@ka="comsalary-blocker2-jobname%d"]//text()' % k).extract()[0]
            items['salary'] = tr[i].xpath('descendant::td[@class="s-d-average"]//text()')[0].extract()
            yield items