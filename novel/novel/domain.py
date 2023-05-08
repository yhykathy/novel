'''
1、生成url数据表
2、数据表处理
3、读取数据表，获取文本并处理
4、下载文本
'''
import fnmatch
import subprocess
import sys
sys.path.append(r"E:\reptile\novel\novel\settings.py")
import csv
import random
from novel.novel.send import Send
from lxml import etree
import requests
from bs4 import BeautifulSoup
import os
import pandas as pd

#103行count定位需变换
# 需要删除的文本
slip = "最新网址"
# 文章链接
url_sum = "https://www.aixiaxs.info/84/84204/"
# 文章标题
name = "在逃生游戏中做朵黑心莲"

# 文件地址
excel_path = r"./spiders/novel.csv"
# 构造请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
    'Connection': 'close',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Referer': url_sum,
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.9'
}
# 代理列表
user_agent_list = [
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0;) Gecko/20100101 Firefox/61.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
]
# 随机选取一个代理，总是使用同一个容易被封
headers['User-Agent'] = random.choice(user_agent_list)

#生成url数据，暂时手动
def one():
    os.system(r"cd E:/reptile/novel/novel/spiders && scrapy crawl novel_spider -o novel.csv")

# 2、数据处理
def two():
    # novel.csv第三列元素进行从大到小排序并绘制图像
    txt = pd.read_csv(excel_path, header=0, usecols=[0, 1])
    # 去重，按照subset指定列进行去重
    txt.drop_duplicates(subset=['title', 'title_href'], keep='first', inplace=True)
    # 排序，默认升序,ascending=False指定降序排列即按照从大到小进行排序
    txt_2 = txt.sort_values(by=["title_href"], ascending=True)
    flag = "第一章" not in txt_2.values.tolist()[0][0] and "第1章" not in txt_2.values.tolist()[0][0] and "第 1 章" not in txt_2.values.tolist()[0][0] and "第 一 章" not in txt_2.values.tolist()[0][0]
    if flag:
        txt_2 = txt.sort_values(by=["title_href"], ascending=False)
    # 表头
    header = ['标题', '地址']
    # 生成新的csv文件
    with open(r'D:\book\title.csv', 'w', encoding='utf-8', newline='') as file_obj:
        # 创建对象
        writer = csv.writer(file_obj)
        # 写表头
        writer.writerow(header)
        # 3.写入数据(一次性写入多行)
        writer.writerows(txt_2.values)
    title = pd.read_csv(r'D:\book\title.csv', header=0, usecols=[0]).values.tolist()
    url = pd.read_csv(r'D:\book\title.csv', header=0, usecols=[1]).values.tolist()
    # print(title,url)
    return title,url

# 删除文件夹中过期数据表
def del_file(path):
    for i in [txt for txt in os.listdir(path) if fnmatch.fnmatch(txt, '*.csv')]:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):#如果是文件夹那么递归调用一下
            del_file(c_path)
        else:                    #如果是一个文件那么直接删除
            os.remove(c_path)
    print ('文件已经清空完成')

# 3、读取数据表，获取文本并处理
def download(url,title):
    res = requests.get(url=url, headers=headers, timeout=10)
    # 防止乱码
    html = etree.HTML(res.text)
    if res.status_code != 200:
        print("爬取失败")
    html = res.content
    soup = BeautifulSoup(html, 'html.parser')
    # 获取内容,并处理
    # s = soup.find_all(class_='yd_text2')[0].text
    s = soup.find_all(id='content')[0].text
    s = s.replace("<br/><br/>", "于鸿玥")
    s = s.replace("<br/>", "")
    s = s.replace("<br/>", "")
    s = s.replace("　　", "于鸿玥")
    s = s.replace("    ", "于鸿玥")
    s = s.replace("  ", "于鸿玥")
    s = s.replace("</p><p>", "于鸿玥")
    s = s.replace("<p>", "")
    s = s.replace("</p>", "")
    s = s.replace(url.replace("www.123wx.cc","123wx.cc"), "")
    info=""
    for n in range(0, len(s) - 1):
        # 判断字符是否为汉字，中文标点，字母
        if '\u4e00' <= s[n] <= '\u9fff' or s[n] in '：，,:.%；”“？！。' or s[n].isalpha():
            info += s[n]
    # 删除后缀不是内容的文本
    content = info.split(slip)[0]
    # 换行
    content = content.replace("于鸿玥", "\n")
    # 设置下载路径
    path = r'D:\book/' + name + '.txt'
    if not os.path.exists(r'D:\book'):
        os.mkdir(r'D:\book')
    # 下载到文件
    with open(path, 'a', encoding="utf-8") as f:
        f.write(title + "\n\n")
        f.write(content)
        f.write("\n")
        f.close()

# 4、下载文本
def domain():
    one()
    title, url = two()
    if os.path.exists(r'D:\book\{}.txt'.format(name)):
        with open(r'D:\book\{}.txt'.format(name), 'r+') as file:
            file.truncate(0)
    for i in range(len(url)):
    # for i in range(1):
        urls = "https://www.aixiaxs.info"+url[i][0]
        try:
            download(urls, title[i][0])
        except Exception as e:  # 捕获异常并打印异常信息，跳过该url
            print(urls + '  ' + str(e))
        print(title[i][0] +' 下载完成,地址为：' + urls)
    print('**下载完成**')
    del_file("./spiders")

if __name__ == '__main__':
    domain()
    se = Send()
    file1 = r'D:\book\{}.txt'.format(name)  # 文件路径
    # file1 = r'E:\picture\结果2023-03-29-13-42-48.png'  # 文件路径
    who = '文件传输助手'     # 适用于中文版微信
    se.send_file_to_single_user(file=file1,message="文件到了，请查收~" ,who=who)

