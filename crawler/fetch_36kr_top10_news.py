import requests
from bs4 import BeautifulSoup
import json
import csv
from datetime import datetime

def crawl_36kr_ai_news():
    # 目标URL
    url = 'https://36kr.com/information/AI/'
    
    # 设置请求头，模拟浏览器访问
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
    }
    
    try:
        # 发送HTTP请求
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # 确保页面编码正确
        response.encoding = 'utf-8'
        
        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 找到新闻列表容器
        news_items = []
        
        # 根据页面结构获取新闻条目
        article_elements = soup.select('div.information-flow-list a.article-item-title')
        
        # 限制只获取前10条
        count = 0
        for article in article_elements:
            if count >= 10:
                break
                
            title = article.get_text().strip()
            link = article['href']
            
            # 处理相对URL
            if link.startswith('/'):
                link = 'https://36kr.com' + link
            
            news_items.append({
                'title': title,
                'link': link
            })
            count += 1
        
        # 输出结果
        print(f"成功获取{len(news_items)}条36氪AI资讯")
        
        # 同时打印到控制台
        print("\n36氪AI资讯前10条:")
        for i, item in enumerate(news_items, 1):
            print(f"{i}. {item['title']}")
            print(f"   链接: {item['link']}")
            print()
            
        return news_items
        
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
        return []
    except Exception as e:
        print(f"发生错误: {e}")
        return []