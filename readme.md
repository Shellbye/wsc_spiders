scrapy_wsc
==========

usage
-----

> - use `sudo apt-get install python-pip` to install pip, or read [this][2] for more info
> - use `sudo pip install -r required.txt` to install required third packages
> - (optional) run `python insert_ids.py` to import some initial id in **zhihu_user_data_ids**
> - use `nohup python bgservice.py &` to start the scrapy


development
-----------

> - use `scrapy startproject myproject` to start new project
> - use `scrapy genspider mydomain mydomain.com` to create new spider of domain `mydomain`
> - use `scrapy shell "http://www.shellbye.com/blog/"` to test logic
> - use `scrapy crawl spider_name` to start crawl
> - full command list check [here][1]


[1]:http://doc.scrapy.org/en/0.24/topics/commands.html
[2]:https://pip.pypa.io/en/latest/installing.html