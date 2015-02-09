__author__ = 'shellbye'
# -*- coding:utf-8 -*-
# https://github.com/yoyzhou/weibo_login
import time
import os
import urllib
import urllib2
import cookielib
import base64
import re
import hashlib
import json
import rsa
import binascii
import scrapy
from scrapy.http import Request
from scrapy.http import FormRequest
from pymongo import MongoClient

from wsc.settings import IP, DB, DEBUG


def get_pwd_rsa(pwd, servertime, nonce, weibo_rsa_n):
    """
        Get rsa2 encrypted password, using RSA module from https://pypi.python.org/pypi/rsa/3.1.1,
        documents can be accessed at
        http://stuvel.eu/files/python-rsa-doc/index.html
    """
    weibo_rsa_e = 65537
    message = str(servertime) + '\t' + str(nonce) + '\n' + str(pwd)
    key = rsa.PublicKey(int(weibo_rsa_n, 16), weibo_rsa_e)
    encropy_pwd = rsa.encrypt(message, key)
    return binascii.b2a_hex(encropy_pwd)


def get_user(username):
    username_ = urllib.quote(username)
    username = base64.encodestring(username_)[:-1]
    return username


class ProxyTestSpider(scrapy.Spider):
    name = "weibo_info"
    if DEBUG:
        collection = "weibo_debug"
    else:
        collection = "weibo"
    weibo_user_ids = MongoClient(IP, 27017)[DB]['weibo_user_ids']
    unique_key = 'user_id'
    username = '444854713@qq.com'
    pwd = '288664'
    allowed_domains = ["weibo.com", 'sina.com.cn', 'weicaifu.com', '97973.com']
    start_urls = (
        'http://www.weibo.com/',
    )

    def parse(self, response):
        # print "parse: " + response.url
        # print response.request.cookies
        # pre_login_url = "http://login.sina.com.cn/sso/prelogin.php?" \
        #                 "entry=weibo&" \
        #                 "callback=sinaSSOController.preloginCallBack&" \
        #                 "su=" + str(get_user(self.username)) + "&" \
        #                 "rsakt=mod&" \
        #                 "checkpin=1&" \
        #                 "client=ssologin.js(v1.4.18)&" \
        #                 "_=" + str(time.time())
        cookie_jar = cookielib.LWPCookieJar("weibo_login_cookies.dat")
        cookie_jar.load(ignore_discard=True, ignore_expires=True)
        yield Request("http://weibo.com/u/2159629311", callback=self.parse_2, meta={'cookiejar': cookie_jar})

    def parse_2(self, response):
        print "parse_2: pre_login"
        print response.body
        # print response.body
    #     p = re.compile('\((.*)\)')
    #     json_data = p.search(response.body).group(1)
    #     data = json.loads(json_data)
    #     # print data
    #     servertime = str(data['servertime'])
    #     nonce = data['nonce']
    #     rsakv = data['rsakv']
    #     pubkey = data['pubkey']
    #     pcid = data['pcid']
    #     # print pcid
    #     login_url = "http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)"
    #     login_data = {
    #         'entry': 'weibo',
    #         'gateway': '1',
    #         'from': '',
    #         'savestate': '7',
    #         'userticket': '1',
    #         'pagerefer': '',
    #         'pcid': pcid,
    #         'door': "z3wcc",
    #         'vsnf': '1',
    #         'su': get_user(self.username),
    #         'service': 'miniblog',
    #         'servertime': servertime,
    #         'nonce': nonce,
    #         'pwencode': 'rsa2',
    #         'rsakv': rsakv,
    #         'sp': get_pwd_rsa(self.pwd, servertime, nonce, pubkey),
    #         'sr': '1920*1080',
    #         'encoding': 'UTF-8',
    #         'prelt': '45',
    #         'url': 'http://weibo.com/ajaxlogin.php?'
    #                'framelogin=1&'
    #                'callback=parent.sinaSSOController.feedBackUrlCallBack',
    #         'returntype': 'META'
    #     }
    #     yield FormRequest(login_url, formdata=login_data, callback=self.parse_3)
    #
    # def parse_3(self, response):
    #     print "parse_3: " + response.url
        # print "\n" + response.body
        # url = "http://passport.weibo.com/wbsso/login?" \
    #           "ssosavestate=1454478561&" \
    #           "url=" + urllib.quote('http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack&sudaref=weibo.com') + "&" \
    #           "ticket=ST-MTc2OTc0MzA2NQ&" \
    #           "retcode=0"
    #
    #     yield Request(url, callback=self.parse_4)
    #
    # def parse_4(self, response):
    #     print "parse_4: " + response.url
    #     print response.body
    #     check_url = "http://weibo.com/u/2159629311"
    #     yield Request(check_url, callback=self.parse_5)
    #
    # def parse_5(self, response):
    #     print response.body