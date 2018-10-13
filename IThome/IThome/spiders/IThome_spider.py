# -*- coding: utf-8 -*-
import json
import re

import scrapy
from bs4 import BeautifulSoup

from IThome.items import IthomeItem


def get_hot_comment(response):
    # print(response.text)
    title = response.meta['title']
    item = IthomeItem()
    item['title'] = title
    # 分析response.text，发现为json格式,'html'对应html源码,即{'html':<li>...}
    html = json.loads(response.text)['html']
    # html源码格式化
    soup = BeautifulSoup(html, 'lxml')
    # 每条热评在class='entry'的li标签内
    li_list = soup.find_all('li', class_='entry')
    for li in li_list:
        # 分析html源码，取出热评对应数据
        item['username'] = li.find('span', class_='nick').text
        item['time'] = li.find('span', class_='posandtime').text.split('\xa0')[1]
        item['content'] = li.find('p').text
        like = li.find('a', class_='s').text
        hate = li.find('a', class_='a').text
        # 选出点赞数和反对数,例:支持(100)匹配出100
        item['like_num'] = re.search(r'\d+', like).group()
        item['hate_num'] = re.search(r'\d+', hate).group()
        # print(item)
        yield item

    # 下面为最开始直接根据xpath选出对应数据，试验发现无数据，最后发现
    # 返回的response不是标准的html格式,所以这种方法行不通
    # li_list = response.xpath('//*[@id="ulhotlist"]/li')
    # for li in li_list:
    #     item['username'] = li.xpath('./div/div[2]/div[1]/div/span[1]/a/text()').extract()[0]
    #     item['time'] = li.xpath('./div/div[2]/div[1]/div/span[2]/text()').extract()[0].split(' ')[1]
    #     item['content'] = li.xpath('./div/div[2]/p/text()').extract()[0]
    #     like = li.xpath('./div/div[2]/div[2]/div[2]/span/a[1]/text()').extract()[0]
    #     hate = li.xpath('./div/div[2]/div[2]/div[2]/span/a[2]/text()').extract()[0]
    #     item['like_num'] = re.search(r'\d+',like)
    #     item['hate_num'] = re.search(r'\d+',hate)
    #     print(item)
    #     yield item


def get_commit_hash(response):
    title = response.meta['title']
    newsID = response.meta['newsID']
    # hash在script标签内
    script = response.xpath('/html/head/script[3]/text()').extract()[0]
    # 选出hash,例:var ch11 = '0A56BCA76AE1AD61';匹配出0A56BCA76AE1AD61
    pattern = re.compile(r'\w{16}')
    hash = pattern.search(script).group()
    # print(hash)
    post_url = 'https://dyn.ithome.com/ithome/getajaxdata.aspx'  # post url
    # post数据为newsID,hash,pid,type
    yield scrapy.FormRequest(
        url=post_url,
        meta={'title': title},
        formdata={'newsID': newsID, 'hash': hash, 'pid': '1', 'type': 'hotcomment'},
        callback=get_hot_comment
    )


class IthomeSpiderSpider(scrapy.Spider):
    name = 'IThome_spider'
    # allowed_domains = ['https://www.ithome.com/']
    start_urls = ['https://www.ithome.com/']

    def parse(self, response):
        # 24小时阅读榜的标题和url包含在li标签内
        li_list = response.xpath('//*[@id="con"]/div[5]/div[2]/div[3]/div[3]/div[1]/ul/li')
        for li in li_list:
            link = li.xpath('./a/@href').extract()[0]
            title = li.xpath('./a/@title').extract()[0]
            # 选出newsID，例:https://www.ithome.com/0/388/110.htm匹配出[388,110]
            pattern = re.compile(r'(\d\d\d)')
            newsID_list = pattern.findall(link)
            newsID = newsID_list[0] + newsID_list[1]  # 拼接出newsID
            comment_url = 'https://dyn.ithome.com/comment/' + newsID  # 热评url
            print(comment_url)
            # title和newsID传递给函数,title最后存入数据库,newsID在post中需要
            yield scrapy.Request(comment_url, callback=get_commit_hash, meta={'title': title, 'newsID': newsID})
