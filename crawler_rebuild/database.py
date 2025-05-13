import pymysql
from datetime import datetime, date
from typing import List
from config import DBConfig, NewsArticle


class DatabaseManager:
    def __init__(self, config: DBConfig):
        self.config = config

    def _get_connection(self):
        return pymysql.connect(
            host=self.config.host,
            user=self.config.user,
            password=self.config.password,
            database=self.config.database,
            charset=self.config.charset
        )

    def clear_table(self, table_name: str) -> None:
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(f"DELETE FROM {table_name}")
                    conn.commit()
                    print(f"✅ 已清空 {table_name} 表")
                except Exception as e:
                    print(f"[清空失败] -> {e}")

    def save_article(self, article: NewsArticle) -> None:
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                try:
                    today = date.today()
                    now = datetime.now()

                    sql = """
                          INSERT INTO news_flash
                          (date, region, title, summary, detail, image_url, source_url, created_at)
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s) \
                          """
                    cursor.execute(sql, (
                        today, article.region, article.title, article.summary,
                        article.content, article.image_url, article.link, now
                    ))
                    conn.commit()
                    print(f"✅ 已保存：{article.title}")
                except Exception as e:
                    print(f"[写入失败] {article.link} -> {e}")
