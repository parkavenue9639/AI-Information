from dataclasses import dataclass
from typing import Optional

@dataclass
class DBConfig:
    host: str
    user: str
    password: str
    database: str
    charset: str = 'utf8mb4'

@dataclass
class NewsArticle:
    title: str
    content: str
    link: str
    summary: str = ""
    image_url: str = ""
    region: str = "科技"
