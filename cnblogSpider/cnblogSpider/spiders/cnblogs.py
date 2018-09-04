# -*- coding: utf-8 -*-
import scrapy
from cnblogSpider.items import CnblogspiderItem
from scrapy import Selector

class CnblogsSpider(scrapy.Spider):
    name = 'cnblogs'
    allowed_domains = ['cnblogs.com']
    start_urls = ['http://cnblogs.com/LouieZhang/']

    def parse(self, response):
        #找到所有文章
        papers = response.xpath('//*[@class="day"]')
        #提取文章链接、标题和摘要
        for paper in papers:
            url = paper.xpath('.//*[@class="postTitle"]/a/@href').extract()[0]
            title = paper.xpath('.//*[@class="postTitle"]/a/text()').extract()[0]
            summary = paper.xpath('.//*[@class="postCon"]/div/text()').extract()[0]
            item = CnblogspiderItem(url=url,title=title,summary=summary)
            request=scrapy.Request(url = url,callback=self.parse_body)
            request.meta['item'] = item #将item暂存
            yield item

        #找下一页超链
        next_page = Selector(response).re(u'<a href = "(\S*)"下一页</a>')
        if next_page:
            yield scrapy.Request(next_page,callback = self.parse)

    def parse_body(self,response):
        item = response.meta['item']
        body = response.xpath('.//div[@class="postDesc"]/a/text()')
        item['body'] = body
        yield item





