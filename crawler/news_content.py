import asyncio
import csv
from playwright.async_api import async_playwright

async def extract_36kr_article(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, timeout=60000)

        # 等待正文加载
        await page.wait_for_selector('div.article-content', timeout=60000)

        title = await page.title()
        content = await page.inner_text('div.article-content')

        await browser.close()
        return title, content

async def a_get_news_content(news_items):
    async def process_item(item):
        try:
            title, content = await extract_36kr_article(item['link'])
            return {'title': title, 'content': content, 'link': item['link']}
        except Exception as e:
            print(f"抓取失败：{item['link']}，原因：{e}")
            return None

    # 并发执行所有任务
    results = await asyncio.gather(*[process_item(item) for item in news_items])
    # 过滤掉失败的结果（None值）
    return [r for r in results if r is not None]