# -*- coding: utf-8 -*-
import json
import urllib2

if __name__ == "__main__":
    _xsrf = 'f1460d2580fbf34ccd508eb4489f1097'
    url = 'http://www.zhihu.com/node/ProfileFolloweesListV2'
    offset = 20
    params = json.dumps(
        {
            "offset": str(offset),
            "order_by": "created",
            "hash_id": '18c79c6cc76ce8db8518367b46353a54'
        }
    )
    post_params = {"params": params, "method": "next", "_xsrf": _xsrf}
    ret = urllib2.urlopen(url, post_params)
    print ret