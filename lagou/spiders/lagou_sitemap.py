#encoding=utf-8
import re

__author__ = 'Administrator'
import math
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import Rule
from scrapy.selector import Selector
from ..items import CompanyItem
import scrapy

class TestSpider(scrapy.Spider):
    name = 'lagou_sitemap'
    collection = 'lagou_sitemap'
    unique_key = 'id'
    allowed_domains = ['lagou.com']
    start_urls = ['http://www.lagou.com/sitemap/']

    def parse(self, response):
        # xp = Selector(response)
        # site = xp.xpath("//a[contains(@href, 'http://www.lagou.com/c/')]")
        # for x in site:
        #     url = x.xpath('./@href')[0].extract()
        #     pattern = re.compile(r'http://www.lagou.com/c/\d{1,5}.html')
        #     reurl = pattern.findall(url)
        #     if reurl:
        #         url = reurl[0].replace("http://www.lagou.com/c/","http://www.lagou.com/gongsi/")
        #         yield scrapy.Request(url, callback=self.parse_info, meta={'url': url})
        body = response.body
        pattern = re.compile(r'http://www.lagou.com/c/\d{1,5}.html')
        reurls = pattern.findall(body)
        for reurl in reurls:
            url = reurl.replace("http://www.lagou.com/c/","http://www.lagou.com/gongsi/")
            yield scrapy.Request(url, callback=self.parse_info, meta={'url': url})

    #test one url
    # def parse(self, response):
    #     url = u'http://www.lagou.com/gongsi/451.html'
    #     yield scrapy.Request(url, callback=self.parse_info, meta={'url': url})

    def parse_info(self, response):
        select = Selector(response)
        company = CompanyItem()
        field = {}
        field.setdefault('title',"//h2/text()")
        field.setdefault('vali',"//span[@class='va dn']/text()")
        field.setdefault('fullname',"//h1/text()")
        field.setdefault('introduction',"//div[@class='c_intro']/text()")
        field.setdefault('id',"//input[@type='hidden']//@value")
        field.setdefault('stage',"//ul[@class='reset stageshow']/li/span/text()")
        field.setdefault('homepage',"//div[@class='c_tags']/table/tr/td/a/@href")
        for key,value in field.iteritems():
            s = select.xpath("%s" %value)
            if s:
                company['%s' %key] = s[0].extract()
        company['url'] = response.meta['url']
        s = select.xpath("//div[@class='clear oneword']/text()")
        if s:
            company['brief'] = s[0].extract().replace(u'\xa0',"")
        labels = []
        s = select.xpath("//ul[@id='hasLabels']/li/span/text()")
        if s:
            for x in s:
                labels.append(x.extract())
        company['labels'] = labels
        s = select.xpath("//span[@class='jobsTotal']/i/text()")
        if s:
            company['jobCount'] = s[0].extract()
        else:
            company['jobCount'] = u"0"
        s = select.xpath("//div[@class='c_tags']/table/tr/td/text()")
        if s:
            company['location'] = s[1].extract()
            company['field'] = s[3].extract()
            company['size'] = s[5].extract().replace(u'\t',"").replace(u'\r\n',"").replace(u' ',"")

        joblist = []
        s = select.xpath("//ul[@id='jobList']/li/a")
        if s:
            for x in s:
                job = {}
                job['jobname'] = x.xpath("./h3/span[1]/text()")[0].extract()
                job['joblocation'] = x.xpath("./h3/span[2]/text()")[0].extract().replace("[","").replace("]","")
                job['jobrequirement'] = x.xpath("./div/text()")[0].extract().replace(u'\t',"").replace(u'\r\n',"").replace(u' ',"")
                job['time'] = x.xpath("./span/text()")[0].extract()
                joblist.append(job)
        company['jobList'] = []
        pageNo = int(math.ceil(float(company['jobCount'])/10))
        for i in range(1,pageNo+1):
            url = "http://www.lagou.com/jobs/pl_%s.html?pageNo=%s" %(company['id'],i)
            yield scrapy.Request(url=url,callback=self.getJobList,meta={"company":company})

    def getJobList(self, response):
        company = response.meta['company']
        select = Selector(response)
        s = select.xpath("//ul[@class='reset c_jobs']/li/a")#获得职位列表
        if s:
            for x in s:
                job_link = x.xpath("./@href")[0].extract()
                #爬取 职位详细信息
                yield scrapy.Request(url=job_link,callback=self.parse_job,meta={"company":company,"job_link":job_link})

    def parse_job(self, response):
        company = response.meta['company']
        job_link = response.meta['job_link']
        select = Selector(response)
        job = {}
        job['job_link'] = job_link
        job['job_name'] = select.xpath("//h1/@title").extract()[0]
        job['jd'] = select.xpath("//dd[@class='job_bt']").extract()[0]
        job['job_request'] = select.xpath("//dd[@class='job_request']").extract()[0]
        company['jobList'].append(job)
        return company
