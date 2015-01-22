__author__ = 'shellbye'
# http://mahmoud.abdel-fattah.net/2012/04/07/using-scrapy-with-proxies/
import random


class ProxyMiddleware(object):
    def process_request(self, request, spider):
        f = open("../files/proxy_ips.txt", 'r')
        proxy_pool = f.readlines()
        p = proxy_pool[random.randint(0, len(proxy_pool) - 1)]
        request.meta['proxy'] = 'http://' + p.strip()
