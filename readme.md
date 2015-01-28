scrapy_wsc
==========

usage
-----

> - use `sudo apt-get install python-pip` to install pip, or read [this][2] for more info
> - use `sudo pip install -r required.txt` to install required third packages
> - (optional) run `python insert_ids.py` to import some initial id in **zhihu_user_data_ids**
> - (not used) use `nohup python start.py &` to start the scrapy
> - (not used) use `sudo kill $(ps aux | grep 'python start.py' | awk '{print $2}')` to kill all process
> - (not used) use `ps aux | grep start.py` to check id pid of the previous program(1st column)
> - (not used) use `sudo kill -9 pid` to stop the program
> - user `kill -9 $(ps aux | grep 'supervisord' | awk '{print $2}')` to kill supervisord
> - use `supervisord` in current work directory to start the program
> - open `http://localhost:9001` with user/password in supervisord.conf to check status


development
-----------

> - use `scrapy startproject myproject` to start new project
> - use `scrapy genspider mydomain mydomain.com` to create new spider of domain `mydomain`
> - use `scrapy shell "http://www.shellbye.com/blog/"` to test logic
> - use `scrapy crawl spider_name` to start crawl
> - full command list check [here][1]


[1]:http://doc.scrapy.org/en/0.24/topics/commands.html
[2]:https://pip.pypa.io/en/latest/installing.html