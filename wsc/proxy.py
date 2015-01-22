__author__ = 'shellbye'
# http://mahmoud.abdel-fattah.net/2012/04/07/using-scrapy-with-proxies/
import random


class ProxyMiddleware(object):
    def process_request(self, request, spider):
        proxy_pool = [
            '183.41.137.111:3128',
            '1.173.209.129:9064',
            '190.121.117.115:9064',
            '122.121.244.102:8088',
            '114.26.249.239:9064',
        ]
        p = proxy_pool[random.randint(0, len(proxy_pool) - 1)]
        print "---" + p
        request.meta['proxy'] = 'http://' + p
