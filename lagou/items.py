# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LagouItem(scrapy.Item):
    # define the fields for your item here like:
    category = scrapy.Field()
    sub_category = scrapy.Field()
    keywords = scrapy.Field()
    keywords_link = scrapy.Field()
    job_link = scrapy.Field()
    job_name = scrapy.Field()
    jd = scrapy.Field()

class CompanyItem(scrapy.Item):
    id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()  # <h2 title="XXXX">
    fullname = scrapy.Field()  # class="fullname"
    vali = scrapy.Field()  # <span class="va dn"
    brief = scrapy.Field()  # clear oneword
    labels = scrapy.Field()  # hasLabels
    location = scrapy.Field()  # class="c_tags"
    field = scrapy.Field()  # class="c_tags"
    size = scrapy.Field()  # class="c_tags"
    homepage = scrapy.Field()  # class="c_tags"
    introduction = scrapy.Field()  # class="c_intro"
    jobCount = scrapy.Field()  # class="jobsTotal"
    jobList = scrapy.Field()  # id="jobList"
    stage = scrapy.Field()  # class="reset stageshow"
    member_info = scrapy.Field()  # class="member_info noborder"


class Job(scrapy.Item):  # id="jobList"
    jobname = scrapy.Field()
    joblocation = scrapy.Field()
    jobrequirement = scrapy.Field()
    time = scrapy.Field()