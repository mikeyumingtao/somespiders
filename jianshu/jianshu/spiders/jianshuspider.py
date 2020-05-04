# -*- coding: utf-8 -*-
import scrapy
from jianshu.items import JianshuItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import my_fake_useragent as ua


class JianshuspiderSpider(CrawlSpider):
    name = 'jianshuspider'
    allowed_domains = ['jianshu.com']
    start_urls = ['http://jianshu.com/']
    custom_settings = {"USER_AGENT": ua.UserAgent().random()}

    rules = (
        Rule(LinkExtractor(allow=r'.*?/p/.*?'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        title = response.xpath('//h1[@title]/text()').get()
        # 文章标题
        author = response.xpath('//div[@class]/a[@href]/span[@class]/text()').get()
        # 文章作者

        # 用于存储文章内容
        x_content = response.xpath('//article//text()').getall()
        content = ' '.join(x_content)
        print(title, author, content)
        item = JianshuItem(title=title, author=author, content=content)
        yield item

