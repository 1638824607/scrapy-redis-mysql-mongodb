# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class DmozItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()


class BookItem(scrapy.Item):
    # 小说链接
    book_url = scrapy.Field()
    # 小说作者
    author_name = scrapy.Field()
    # 小说名称
    name = scrapy.Field()
    # 小说简介
    description = scrapy.Field()
    # 小说封面图
    cover = scrapy.Field()
    # 小说字数
    word_count = scrapy.Field()
    # 小说最后章节
    latest_chapter_id = scrapy.Field()


class BookChapterItem(scrapy.Item):
    # 小说url redis标示
    book_url = scrapy.Field()
    # 小说名称 打日志
    book_name = scrapy.Field()
    # 章节标题
    name = scrapy.Field()
    # 章节mongo_id
    db_id = scrapy.Field()
    # 小说章节名称
    book_id = scrapy.Field()
    # 章节字数统计
    word_count = scrapy.Field()
    # 章节入库时间
    created_at = scrapy.Field()
    # 章节更新时间
    updated_at = scrapy.Field()
    # 小说章节内容
    content = scrapy.Field()