# AI行业每日简讯自动生成与展示系统

## 项目简介

本项目旨在每日自动抓取国内外主流新闻平台的AI领域资讯，利用大语言模型（LLM）自动摘要、精简、分类，生成20条（国内10条、国外10条）权威、精炼的AI行业简讯，并通过网页美观展示，支持图文并茂和详细介绍。

---

## 系统架构

- **前端**：Vue3 + Element Plus（或Ant Design Vue），实现极简美观的资讯展示页面。
- **后端**：Django + Django REST Framework，负责API接口、定时任务、数据抓取与处理、数据存储。
- **数据库**：MySQL，存储每日简讯及相关信息。
- **大模型**：Langchain对接本地或云端LLM（如GPT-4），用于新闻摘要与润色。
- **图片处理**：优先使用新闻原图，无则用AI生成或图库图片。

---

## 核心流程

1. **新闻抓取**
   - 每天定时自动抓取指定新闻平台（如新浪科技、36氪、The Verge、TechCrunch等）AI相关资讯。
   - 支持RSS、API或网页爬虫多种方式。

2. **内容处理与摘要**
   - 对抓取到的新闻内容，调用LLM进行自动摘要、精简为60字以内的简讯，并自动分类为"国内"或"国外"。
   - LLM可同时生成更吸引人的标题和详细介绍。

3. **配图处理**
   - 优先使用新闻原文配图，无配图时可调用AI图片生成或图库API。

4. **数据存储**
   - 将最终生成的简讯（标题、正文、标签、详细介绍、配图、原文链接等）存入MySQL数据库。
   - 每天自动覆盖旧数据，保留最近N天历史数据。

5. **前端展示**
   - 首页展示当天20条简讯（国内/国外分组），每条显示标题、正文、配图缩略图。
   - 点击简讯可查看详细介绍和大图。
   - UI极简，支持响应式布局。

---

## 数据结构设计（MySQL）

**news_flash表：**

| 字段名         | 类型           | 说明           |
| -------------- | -------------- | -------------- |
| id             | int, PK, AI    | 主键           |
| date           | date           | 日期           |
| region         | varchar(10)    | 国内/国外      |
| title          | varchar(100)   | 标题           |
| summary        | varchar(60)    | 简讯正文       |
| detail         | text           | 详细介绍       |
| image_url      | varchar(255)   | 配图链接       |
| source_url     | varchar(255)   | 原新闻链接     |
| created_at     | datetime       | 创建时间       |

---

## 主要技术实现

### 1. 新闻抓取
- Python爬虫（requests+BeautifulSoup、scrapy）或第三方API（如NewsAPI、Bing News Search API）。
- 支持多平台、多源抓取，自动去重、筛选AI相关内容。

### 2. LLM摘要与分类
- Langchain集成大模型，自动摘要、分类、润色新闻内容。
- Prompt设计：输入新闻标题和正文，输出60字以内简讯、标题、分类。

### 3. 后端API
- Django REST Framework提供RESTful接口，支持前端获取简讯列表、详情。
- 提供手动触发简讯生成的接口，便于测试和调试。

### 4. 前端展示
- Vue3实现极简资讯卡片、弹窗等组件。
- Axios请求后端API，展示数据。
- 响应式布局，适配PC和移动端。

### 5. 定时任务与自动化
- 使用Django-celery-beat或APScheduler实现每日定时任务。
- 自动抓取、摘要、入库、清理历史数据。

---

## 接口设计示例

- `GET /api/newsflash/?date=2024-04-17` 获取当天简讯列表
- `GET /api/newsflash/{id}/` 获取简讯详情
- `POST /api/newsflash/generate/` 手动生成简讯（测试用）

---

## 可选扩展

- 支持历史简讯查询与回顾
- 多语言界面切换
- 用户自定义订阅关键词
- 收藏、分享等交互功能 