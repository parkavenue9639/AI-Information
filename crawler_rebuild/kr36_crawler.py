from playwright.async_api import async_playwright
import asyncio
from bs4 import BeautifulSoup
from base_crawler import BaseCrawler
from config import NewsArticle
from typing import List, Dict

class Kr36Crawler(BaseCrawler):
    def __init__(self):
        super().__init__('https://36kr.com/information/AI/')

    def get_news_list(self, limit: int = 10) -> List[Dict[str, str]]:
        try:
            response = self._make_request(self.base_url)
            soup = BeautifulSoup(response.text, 'html.parser')

            news_items = []
            article_elements = soup.select('div.information-flow-list a.article-item-title')

            for article in article_elements[:limit]:
                title = article.get_text().strip()
                link = article['href']

                if link.startswith('/'):
                    link = 'https://36kr.com' + link

                news_items.append({
                    'title': title,
                    'link': link
                })

            print(f"成功获取{len(news_items)}条36氪AI资讯")
            return news_items

        except Exception as e:
            print(f"获取新闻列表失败: {e}")
            return []

    async def get_article_content(self, url: str) -> NewsArticle:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            try:
                await page.goto(url, timeout=60000)
                await page.wait_for_selector('div.article-content', timeout=60000)

                title = await page.title()
                content = await page.inner_text('div.article-content')

                return NewsArticle(title=title, content=content, link=url)
            finally:
                await browser.close()
