scrapy_wsc
==========

usage
-----



> - use `sudo apt-get install python-pip` to install pip, or read [this][2] for more info
> - use `sudo pip install -r required.txt` to install required third packages
> - (optional) run `python insert_ids.py` to import some initial id in **zhihu_user_data_ids**
> - use `sudo ./start.py` to start the scrapy


development
-----------

> - use `scrapy startproject myproject` to start new project
> - use `scrapy genspider mydomain mydomain.com` to create new spider of domain `mydomain`
> - use `scrapy shell "http://www.shellbye.com/blog/"` to test logic
> - use `scrapy crawl spider_name` to start crawl
> - full command list check [here][1]


work flow
----

```flow
st=>start: Start
e=>end
cond=>condition: Master?
op=>operation: python insert_ids.py
op2=>operation: sudo ./start.py


st->cond
cond(yes)->op
cond(no)->op2
op2->e
op->op2
```


[1]:http://doc.scrapy.org/en/0.24/topics/commands.html
[2]:https://pip.pypa.io/en/latest/installing.html