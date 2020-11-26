import scrapy
from first.items import DmozItem

class DmozSpider(scrapy.Spider):
    
    """ 定义的第一部分：表示从哪里开始 """
    '''
    这里的name 就是对应下一步 scrapy crawl <name_value>
    name必须是唯一的，就像网页的ID，用来确认蜘蛛的名字
    '''
    name = "dmoz"
    #allowed_domains = ["dmoz-odp.org"] # 爬取的一个范围，表示在这个域名下进行爬取
    allowed_domains = ["https://dmoz-odp.org"] # 爬取的一个范围，表示在这个域名下进行爬取
    start_urls      = [               #爬取的开始网址,表示从哪里去爬取
                       "https://www.dmoz-odp.org/Computers/Programming/Languages/Python/Books/",
                       "https://www.dmoz-odp.org/Computers/Programming/Languages/Python/Resources/"
                      ]

    """ 定义一个分析的方法，只有一个response参数 """
    def parseold(self, response):
        filename = response.url.split("/")[-2] # [-2]: Books or Resources
        with open(filename, "wb") as f:
            f.write(response.body)

    def parse(self, response):
        sel = scrapy.selector.Selector(response)
        sites = sel.xpath('//div/div/div/div[@class = "title-and-desc"]')
        items = list()
        for sindex,site in enumerate(sites):
            item  = DmozItem() #实例化一个类对象
            title = site.xpath('a/div/text()').extract()
            link  = site.xpath('a/@href').extract()      
            desc  = site.xpath('div/text()').extract()   
            item["title"] = [i.strip() for i in title]  
            item["link"]  = [i.strip() for i in link]    
            item["desc"] = [i.strip() for i in desc]
            items.append(item)
        return items    
            #print("{}\nurl: {} status: {}".format("="*30,response.url, response.status))
            #print(sindex,title, link, desc)        
# scrapy crawl dmoz
