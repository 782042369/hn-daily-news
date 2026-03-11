#!/usr/bin/env python3
"""
HN Daily News - 后端主程序
负责RSS抓取、内容提取、AI摘要、Markdown生成
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

import feedparser
import httpx
from bs4 import BeautifulSoup
from openai import OpenAI

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 路径配置
BASE_DIR = Path(__file__).parent.parent
CONFIG_DIR = BASE_DIR / "config"
DATA_DIR = BASE_DIR / "data" / "news"
STATE_FILE = BASE_DIR / "data" / "state.json"

# 确保目录存在
DATA_DIR.mkdir(parents=True, exist_ok=True)

class RSSFetcher:
    """RSS源抓取器"""
    
    def __init__(self, feeds_config: str = None):
        self.feeds_config = feeds_config or str(CONFIG_DIR / "feeds.json")
        self.feeds = self._load_feeds()
        
    def _load_feeds(self) -> List[Dict]:
        """加载RSS源配置"""
        config_path = Path(self.feeds_config)
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def fetch_feed(self, feed_url: str) -> List[Dict]:
        """抓取单个RSS源"""
        try:
            response = httpx.get(feed_url, timeout=10, follow_redirects=True)
            feed = feedparser.parse(response.text)
            
            articles = []
            for entry in feed.entries[:5]:  # 每个源最多5篇
                articles.append({
                    'title': entry.get('title', ''),
                    'link': entry.get('link', ''),
                    'published': entry.get('published', ''),
                    'summary': entry.get('summary', ''),
                    'source': feed.feed.get('title', 'Unknown')
                })
            return articles
        except Exception as e:
            logger.error(f"Failed to fetch {feed_url}: {e}")
            return []
    
    def fetch_all(self) -> List[Dict]:
        """抓取所有RSS源"""
        all_articles = []
        for feed in self.feeds:
            logger.info(f"Fetching: {feed['name']}")
            articles = self.fetch_feed(feed['url'])
            all_articles.extend(articles)
        return all_articles


class ContentExtractor:
    """文章内容提取器"""
    
    @staticmethod
    def extract(url: str) -> Optional[str]:
        """提取文章正文内容"""
        try:
            response = httpx.get(url, timeout=10, follow_redirects=True)
            soup = BeautifulSoup(response.text, 'lxml')
            
            # 移除脚本和样式
            for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
                tag.decompose()
            
            # 尝试提取主要内容
            article = soup.find('article') or soup.find('main') or soup.find('div', class_='content')
            
            if article:
                paragraphs = article.find_all('p')
            else:
                paragraphs = soup.find_all('p')
            
            # 提取段落文本
            content = '\n\n'.join(
                p.get_text().strip() 
                for p in paragraphs[:10] 
                if len(p.get_text().strip()) > 50
            )
            
            return content[:2000] if content else None
            
        except Exception as e:
            logger.error(f"Failed to extract content from {url}: {e}")
            return None


class Summarizer:
    """AI摘要生成器"""
    
    def __init__(self, api_key: str = None):
        self.client = OpenAI(api_key=api_key or os.getenv('OPENAI_API_KEY'))
        
    def summarize(self, title: str, content: str) -> str:
        """生成100-200字摘要"""
        if not content:
            return "（无法获取文章内容）"
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "你是一个专业的科技新闻编辑。请用中文为给定的文章生成100-200字的摘要，突出核心要点。"
                    },
                    {
                        "role": "user",
                        "content": f"标题：{title}\n\n内容：{content}"
                    }
                ],
                max_tokens=300,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Failed to summarize: {e}")
            # 返回前200字符作为备用
            return content[:200] + "..." if len(content) > 200 else content


class NewsGenerator:
    """新闻Markdown生成器"""
    
    @staticmethod
    def generate(articles: List[Dict], output_path: Path = None) -> str:
        """生成Markdown格式的新闻简报"""
        date_str = datetime.now().strftime('%Y-%m-%d')
        date_cn = datetime.now().strftime('%Y年%m月%d日')
        
        md_content = f"""# 📰 HN每日新闻简报
**{date_cn}**

> 为程序员精选的每日技术热点

---

"""
        
        for i, article in enumerate(articles, 1):
            md_content += f"""## {i}. {article['title']}

**来源：** {article['source']}

{article.get('summary', '（暂无摘要）')}

🔗 [阅读原文]({article['link']})

---

"""
        
        md_content += f"""
---

*生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC*
"""
        
        # 保存到文件
        if output_path is None:
            output_path = DATA_DIR / f"hn-daily-{date_str}.md"
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        logger.info(f"News saved to: {output_path}")
        return str(output_path)


def main():
    """主函数"""
    logger.info("🚀 Starting HN Daily News fetch...")
    
    # 1. 抓取RSS
    fetcher = RSSFetcher()
    articles = fetcher.fetch_all()
    logger.info(f"📊 Fetched {len(articles)} articles")
    
    if not articles:
        logger.warning("No articles found!")
        return
    
    # 2. 提取内容和生成摘要
    extractor = ContentExtractor()
    summarizer = Summarizer()
    
    processed_articles = []
    for article in articles[:20]:  # 最多处理20篇
        logger.info(f"Processing: {article['title'][:50]}...")
        
        # 提取内容
        content = extractor.extract(article['link'])
        
        # 生成摘要
        summary = summarizer.summarize(article['title'], content or article['summary'])
        article['summary'] = summary
        
        processed_articles.append(article)
        
    # 3. 生成Markdown
    output_file = NewsGenerator.generate(processed_articles)
    logger.info(f"✅ Done! News saved to: {output_file}")
    
    return output_file


if __name__ == "__main__":
    main()
