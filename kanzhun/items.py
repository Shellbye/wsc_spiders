import scrapy


class KanZhunItem(scrapy.Item):
    name = scrapy.Field()      
    score = scrapy.Field()      
    url = scrapy.Field()        
    industry = scrapy.Field()   
    address = scrapy.Field()    
    scale = scrapy.Field()      
    ceo = scrapy.Field()        
    job = scrapy.Field()        
    salary = scrapy.Field()      
    competitors = scrapy.Field()
    stockName = scrapy.Field()
    stockCode = scrapy.Field()
    stockLocation = scrapy.Field()
    stockValue = scrapy.Field()


class JobItem(scrapy.Item):
    name = scrapy.Field()       
    job = scrapy.Field()        
    salary = scrapy.Field()      