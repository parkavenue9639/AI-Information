import asyncio
from config import DBConfig
from database import DatabaseManager
from kr36_crawler import Kr36Crawler
from news_processor import NewsProcessor


async def main():
    # 配置初始化
    db_config = DBConfig(
        host='localhost',
        user='root',
        password='123456',
        database='ai_news'
    )

    # 创建必要的对象
    db_manager = DatabaseManager(db_config)
    crawler = Kr36Crawler()
    processor = NewsProcessor(crawler, db_manager)

    # 执行爬虫流程
    news_items = processor.get_news_list()
    articles = await processor.process_news_content(news_items)
    processor.save_articles(articles)


if __name__ == '__main__':
    asyncio.run(main())
