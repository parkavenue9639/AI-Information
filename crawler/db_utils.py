# db_utils.py
import pymysql
from datetime import datetime, date

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'ai_news',
    'charset': 'utf8mb4'
}

def clear_news_flash_table():
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM news_flash")
        conn.commit()
        print("✅ 已清空 news_flash 表")
    except Exception as e:
        print(f"[清空失败] -> {e}")
    finally:
        cursor.close()
        conn.close()

def save_article_to_mysql(title, content, link):
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    try:
        today = date.today()
        now = datetime.now()
        region = "科技"
        summary = ""  # 留空，后续用 LLM 生成
        image_url = ""  # 可留空或补充 og:image 提取逻辑

        sql = """
            INSERT INTO news_flash (date, region, title, summary, detail, image_url, source_url, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (
            today, region, title, summary, content, image_url, link, now
        ))
        conn.commit()
    except Exception as e:
        print(f"[写入失败] {link} -> {e}")
    finally:
        cursor.close()
        conn.close()