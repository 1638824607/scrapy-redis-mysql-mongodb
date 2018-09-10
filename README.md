# scrapy-redis-mysql-mongodb
python爬虫框架scrapy异步多进程爬取百万小说同时入mongodb和mysql数据库

# 打印 不输出日志
scrapy crawl dmoz_spider  -s LOG_FILE=all.log 


# 该命令将采用 JSON 格式对爬取的数据进行序列化，生成 items.json 文件。
scrapy crawl dmoz_spider -o items.json
