import scrapy

from ..items import NovelItem


class NovelSpiderSpider(scrapy.Spider):
    name = "novel_spider"
    start_urls = ["https://www.aixiaxs.info/84/84204/"]

    def parse(self, response):
        url_list = response.xpath('//div[@id="list"]/dl/dd/a')
        # 循环电影的条目
        for i_item in url_list:
            # 导入item，进行数据解析
            novel_item = NovelItem()
            novel_item['title'] = i_item.xpath(".//text()").extract_first()
            novel_item['title_href'] = i_item.xpath(".//@href").extract_first()
            print(novel_item)
            yield novel_item
        # 解析下一页，取后一页的XPATH
        next_link = response.xpath("//span[@class='right']/a/@href").extract()
        if next_link:
            next_link = next_link[0]
            yield scrapy.Request(self.start_urls + next_link, callback=self.parse)
