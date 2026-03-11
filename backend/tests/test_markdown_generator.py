"""
单元测试 - Markdown生成模块
"""
import pytest
from datetime import datetime
from pathlib import Path
from modules.markdown_generator import MarkdownGenerator


class TestMarkdownGenerator:
    """Markdown生成器测试"""

    def test_generate(self, tmp_path):
        """测试MD文件生成"""
        generator = MarkdownGenerator(output_dir=tmp_path)
        
        articles = [
            {
                "title": "Test Article",
                "translated_title": "测试文章",
                "link": "https://example.com/test",
                "feed_name": "Test Feed",
                "pub_date": "2026-03-11T10:00:00",
                "summary": "这是一篇测试文章的摘要。",
            }
        ]
        
        filepath = generator.generate(articles, datetime(2026, 3, 11))
        
        assert filepath.exists()
        assert filepath.name == "2026-03-11.md"
        
        content = filepath.read_text(encoding="utf-8")
        assert "HN每日新闻" in content
        assert "测试文章" in content
        assert "https://example.com/test" in content

    def test_format_article(self):
        """测试文章格式化"""
        generator = MarkdownGenerator()
        
        article = {
            "title": "Test",
            "translated_title": "测试标题",
            "link": "https://example.com",
            "feed_name": "Example",
            "summary": "摘要内容",
        }
        
        lines = generator._format_article(article, 1)
        
        assert "## 1. 测试标题" in lines
        assert "**来源：** Example" in lines
        assert "https://example.com" in lines


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
