import os

import pandas as pd
import scrapy

from novel.novel.items import NovelItem

# 文件地址
excel_path = r"./spiders/novel.csv"

class Qtest():
    start_urls = ["https://m.xlaidudu.net/book/22887/"]

    def one(self,response):
        os.system(r"cd E:/reptile/novel/novel/spiders && scrapy crawl novel_spider -o novel.csv")
        # novel.csv第三列元素进行从大到小排序并绘制图像
        txt = pd.read_csv(excel_path, header=0, usecols=[0, 1])
        # 去重，按照subset指定列进行去重
        txt.drop_duplicates(subset=['title', 'title_href'], keep='first', inplace=True)
        # 排序，默认升序,ascending=False指定降序排列即按照从大到小进行排序
        txt_2 = txt.sort_values(by=["title_href"], ascending=True)
        # 循环
        for i_item in txt_2.values.tolist()[1][0]:
            # 导入item，进行数据解析
            novel_item = NovelItem()
            novel_item['count'] = i_item.xpath(".//text()").extract_first()
            print(novel_item)
            # 解析下一页，取后一页的XPATH
            next_link = response.xpath("//a[@id='pb_next]/@href").extract()
            if next_link:
                next_link = next_link[0]
                yield scrapy.Request(self.start_urls + next_link, callback=self.one)