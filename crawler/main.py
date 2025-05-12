import asyncio
from news_content import a_get_news_content
from fetch_36kr_top10_news import crawl_36kr_ai_news
from db_utils import save_article_to_mysql, clear_news_flash_table

# 获取新闻列表
def get_news_list():
    news_items = crawl_36kr_ai_news()
    return news_items

# 获取新闻内容
def get_news_content(news_items):
    res = asyncio.run(a_get_news_content(news_items))
    return res

if __name__ == '__main__':
    news_items = get_news_list()
    full_content_list = get_news_content(news_items)
    print(full_content_list)
    clear_news_flash_table()
    for item in full_content_list:
        save_article_to_mysql(item['title'], item['content'], item['link'])
        print(f"✅ 已保存：{item['title']}")