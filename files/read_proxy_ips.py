__author__ = 'shellbye'
import urllib2
import time
import logging
logging.basicConfig(filename='fetch_ip.log', level=logging.DEBUG)


def fetch_ips():
    get_without_data = urllib2.urlopen("http://erwx.daili666.com/ip/?tid=555852636905661&num=5")
    ips = get_without_data.readlines()
    with open("proxy_ips.txt", 'a') as f:
        f.write('\n')
        for ip in ips:
            f.write(ip)

if __name__ == "__main__":
    for i in range(7, 4000 / 5):
        logging.log(logging.INFO, "fetching the %s time" % i)
        time.sleep(2)
        try:
            fetch_ips()
        except Exception, e:
            logging.log(logging.ERROR, e.message)