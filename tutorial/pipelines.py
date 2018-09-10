# -*- coding: utf-8 -*-
import pymongo
import pymysql
import redis
import time

from tutorial.settings import mongo_host,mongo_port,mongo_db_name,mongo_db_collection
from tutorial.items import BookItem, BookChapterItem
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class TutorialPipeline(object):
    def __init__(self):
        host = mongo_host
        port = mongo_port
        dbname = mongo_db_name
        mongo_collection = mongo_db_collection
        mongo_client = pymongo.MongoClient(host, port)

        self.post = mongo_client[dbname][mongo_collection]

        self.mysql_db = pymysql.connect("10.211.55.5", "root", "root", "book")
        self.mysql_db_cursor = self.mysql_db.cursor()
        self.mysql_db.autocommit(True)

        pool = redis.ConnectionPool(host='10.211.55.5', port=6379)
        self.redis = redis.Redis(connection_pool=pool)

    def process_item(self, item, spider):
        if isinstance(item, BookItem):
            book_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            book_sql = "insert into books(book_url, author_name, name, description, cover, word_count, latest_chapter_id, created_at, updated_at) values ('%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (item['book_url'], item['author_name'], item['name'], item['description'], item['cover'], item['word_count'], item['latest_chapter_id'], book_time, book_time)
            self.mysql_db_cursor.execute(book_sql)

            book_id = self.mysql_db_cursor.lastrowid

            self.redis.set(item['book_url'], book_id)

            print('数据库写入小说《%s》' % item['name'])

        if isinstance(item, BookChapterItem):
            mongo_chapter_data = {
                'content': item['content']
            }

            chapter_id = self.post.insert(mongo_chapter_data)

            book_id = int(self.redis.get(item['book_url']))

            chapter_sql = "insert into chapters(name, db_id, book_id, word_count, created_at, updated_at) values ('%s','%s', '%s', '%s', '%s', '%s')" % (item['name'], str(chapter_id), book_id, item['word_count'], item['created_at'], item['updated_at'])

            print('数据库写入小说《%s》=> 章节(%s)' % (item['book_name'], item['name']))

            self.mysql_db_cursor.execute(chapter_sql)

        return item