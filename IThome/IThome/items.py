# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IthomeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()  # 标题
    username = scrapy.Field()  # 评论人
    time = scrapy.Field()  # 评论时间
    content = scrapy.Field()  # 热评内容
    like_num = scrapy.Field()  # 点赞数
    hate_num = scrapy.Field()  # 反对数
