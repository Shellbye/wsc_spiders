__author__ = 'shellbye'
from scrapy.webservice import JsonResource
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher


class ItemCountResource(JsonResource):

    ws_name = 'item_count'

    def __init__(self, crawler, spider_name=None):
        JsonResource.__init__(self, crawler)
        self.item_scraped_count = 0
        dispatcher.connect(self.scraped, signals.item_scraped)
        self._spider_name = spider_name
        self.isLeaf = spider_name is not None

    def scraped(self):
        self.item_scraped_count += 1

    def render_GET(self, txrequest):
        return self.item_scraped_count

    def getChild(self, name, txrequest):
        return ItemCountResource(name, self.crawler)