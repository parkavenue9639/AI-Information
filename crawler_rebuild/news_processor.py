import asyncio
from typing import List, Dict
from base_crawler import BaseCrawler
from database import DatabaseManager
from config import NewsArticle

class NewsProcessor:
    def __init__(self, crawler: BaseCrawler, db_manager: DatabaseManager):
        self.crawler = crawler
        self.db_manager = db_manager

    def get_news_list(self, limit: int = 10) -> List[Dict[str, str]]:
        return self.crawler.get_news_list(limit)

    async def process_news_content(self, news_items: List[Dict[str, str]]) -> List[NewsArticle]:
        async def process_item(item):
            try:
                return await self.crawler.get_article_content(item['link'])
            except Exception as e:
                print(f"抓取失败：{item['link']}，原因：{e}")
                return None

        results = await asyncio.gather(*[process_item(item) for item in news_items])
        return [r for r in results if r is not None]

    def save_articles(self, articles: List[NewsArticle]) -> None:
        self.db_manager.clear_table('news_flash')
        for article in articles:
            self.db_manager.save_article(article)
