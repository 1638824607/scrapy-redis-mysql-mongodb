# -*- coding: utf-8 -*-
import scrapy
import time
from tutorial.items import BookItem, BookChapterItem
from scrapy.http import Request
import requests
import os
import datetime


class DmozSpider(scrapy.Spider):
    name = "dmoz_spider"
    allow_domains = ['quanbenwu.com']
    start_urls = [
        "http://www.quanbenwu.com/category/2_1_1.aspx",
    ]

    def parse(self, response):
        book_list = response.xpath('/html/body/div[4]/div/div[2]/div')

        for book in book_list:
            book_link = book.xpath('ul/li[1]/strong/a/@href').extract()[0]

            yield Request(url='http://www.quanbenwu.com/' + book_link, callback=self.parse_book_detail)

    def parse_book_detail(self, response):
        # 'www.readnovel.com/book/7661570504015903'
        item = BookItem()
        # 小说链接
        item['book_url'] = response.url
        # 小说作者
        item['author_name'] = response.xpath('//*[@id="bookinfo"]/div[2]/p/text()').extract()[0]
        # 小说名称
        book_name = response.xpath('//*[@id="bookinfo"]/div[2]/h1/text()').extract()[0]
        item['name'] = book_name
        # 小说简介
        book_description = response.xpath('//*[@id="bookintroinner"]').extract()[0]
        item['description'] = book_description

        cover = response.xpath('//*[@id="bookinfo"]/div[1]/img/@src').extract()[0]
        # 小说封面图
        # 下载小说封面图到本地
        now_datetime = datetime.datetime.now()
        new_day = '%s_%s_%s/' % (now_datetime.year, now_datetime.month, now_datetime.day)

        root = "/Users/shenruxiang/my/project/python/scrawl/book_cover/" + new_day
        path = root + cover.split("/")[-1]
        try:
            if not os.path.exists(root):
                os.mkdir(root)
            if not os.path.exists(path):
                r = requests.get(cover)
                r.raise_for_status()
                # 使用with语句可以不用自己手动关闭已经打开的文件流
                with open(path, "wb") as f:  # 开始写文件，wb代表写二进制文件
                    f.write(r.content)
                print("下载小说封面图成功")
            else:
                print("小说封面图已存在")
        except Exception as e:
            print("爬取失败:" + str(e))
            return

        item['cover'] = response.xpath('//*[@id="bookinfo"]/div[1]/img/@src').extract()[0]
        # 小说字数
        book_word_count = response.xpath('//*[@id="bookinfo"]/div[2]/ul/li[3]/label/text()').extract()[0]
        item['word_count'] = book_word_count.replace('万', '')

        # 小说最后章节
        item['latest_chapter_id'] = 0

        yield item

        chapter_list = response.xpath('//*[@id="readlist"]/ul/li')

        for chapter in chapter_list:
            item = BookChapterItem()

            item['book_url'] = response.url
            item['book_name'] = book_name
            # 章节标题
            item['name'] = chapter.xpath('a/text()').extract()[0]
            # 章节字数统计
            # chapter_word_count = re.search(r'章节字数：(.*)', chapter.xpath('a/@title').extract()[0], flags=0)
            item['word_count'] = 0

            chapter_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            # 章节入库时间
            item['created_at'] = chapter_time
            # 章节更新时间
            item['updated_at'] = chapter_time
            # 章节mongo_id
            item['db_id'] = 0
            # 小说章节id
            item['book_id'] = 0

            chapter_url = chapter.xpath('a/@href').extract()[0]

            # yield item
            # print(chapter_url)
            yield Request(url='http://www.quanbenwu.com/' + chapter_url, meta={'item': item}, callback=self.parse_book_chapter_detail)

    # def parse_book_chapter_list(self, response):
    #     # 'www.readnovel.com/book/7661570504015903#Catalog'
    #     chapter_list = response.xpath('//*[@id="j-catalogWrap"]/div[2]/div[1]/ul/li')
    #
    #     for chapter in chapter_list:
    #         item = BookChapterItem()
    #
    #         # 章节标题
    #         item['name'] = chapter.xpath('a/@text()').extract()[0]
    #         # 章节字数统计
    #         chapter_word_count = re.search(r'章节字数：(.*)', chapter.xpath('a/@title').extract()[0], flags=0)
    #         item['word_count'] = chapter_word_count.group(1) if chapter_word_count else 0
    #         # 章节入库时间
    #         item['created_at'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
    #         # 章节更新时间
    #         item['updated_at'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
    #         # 章节mongo_id
    #         item['db_id'] = 0
    #         # 小说章节id
    #         item['book_id'] = 0
    #
    #         chapter_url = chapter.xpath('a/@href').extract()[0]
    #
    #         # yield item
    #         print(chapter_url)
    #         yield Request(url='https:' + chapter_url, meta={'item': item}, callback=self.parse_book_chapter_detail)

    def parse_book_chapter_detail(self, response):
        # item = BookChapterContentItem()
        item = response.meta['item']

        # item['content'] = response.xpath('//*[@id="content"]/p').extract()[0]

        p_list = response.xpath('//*[@id="content"]/p')

        body = ""

        for p in p_list:
            body = body + p.extract()

        item['content'] = body

        yield item