from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup
from config import NewsArticle

class BaseCrawler(ABC):
    def __init__(self, base_url: str, headers: Optional[Dict[str, str]] = None):
        self.base_url = base_url
        self.headers = headers or {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def _make_request(self, url: str) -> requests.Response:
        response = requests.get(url, headers=self.headers, timeout=10)
        response.raise_for_status()
        return response

    @abstractmethod
    def get_news_list(self, limit: int = 10) -> List[Dict[str, str]]:
        pass

    @abstractmethod
    async def get_article_content(self, url: str) -> NewsArticle:
        pass
