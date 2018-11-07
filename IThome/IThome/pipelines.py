# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

import MySQLdb


class IthomePipeline(object):
    def process_item(self, item, spider):
        # 存储到文本
        # base_dir = os.getcwd()
        # filename = base_dir + '/hot_comment.txt'
        # with open(filename,'a') as f:
        #     f.write('标题:{}\n网名:{}\t时间:{}\n热评:{}\n支持:{}\t反对:{}\n\n'.format(
        #         item['title'],item['username'],item['time'],item['content'],item['like_num'],item['hate_num']
        #     ))
        # return item

        # 存储到数据库,ip,user,password,db请换成自己本地数据库
        db = MySQLdb.connect('***', '***', '***', '***', charset='utf8')
        try:
            with db.cursor() as cursor:
                # 请先在数据库建表,建表语句
                # create table if not exists it_home(
                # id int primary key auto_increment,
                # title varchar(50),
                # username varchar(20),
                # time varchar(25),
                # content text,
                # like_num int(6),
                # hate_num int(6))
                sql_insert = 'insert into it_home(title,username,time,content,like_num,hate_num) values(%s,%s,%s,%s,%s,%s)'
                # 防止sql注入，sql语句采用将数据作为execute()的参数,不要采用字符串拼接形式
                # 或者使用cursor提供的insert方法，直接写sql是笔者习惯而已
                cursor.execute(sql_insert, (
                    item['title'], item['username'], item['time'], item['content'], item['like_num'], item['hate_num']))
            db.commit()
            print('title:{},username:{},time:{},content:{},like_num:{},hate_num:{} insert into mysql'.format(
                item['title'], item['username'], item['time'], item['content'], item['like_num'], item['hate_num']
            ))
        except Exception as e:
            print('insert fail,reson:' + e.__str__())
        finally:
            db.close()
        return item
