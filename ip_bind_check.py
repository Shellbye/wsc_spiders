__author__ = 'shellbye'
import sys
import urllib2
import time

if __name__ == "__main__":
    while True:
        time.sleep(60 * 5)
        zhihu = urllib2.urlopen("http://www.zhihu.com")
        if zhihu.code == 200:
            s = "ok " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n"
        else:
            s = "                       bind" + time.strftime("%Y-%m-%d %H:%M:%S") + "\n"
        sys.stdout.write(s)
        sys.stdout.flush()