"""
单元测试 - RSS抓取模块
"""
import pytest
from pathlib import Path
from modules.rss_fetcher import RSSFetcher


class TestRSSFetcher:
    """RSS抓取器测试"""

    def test_parse_opml(self):
        """测试OPML解析"""
        fetcher = RSSFetcher()
        opml_path = Path(__file__).parent.parent.parent / "opml.xml"
        
        if opml_path.exists():
            feeds = fetcher.parse_opml(opml_path)
            assert len(feeds) > 0
            assert all("url" in f and "name" in f for f in feeds)
        else:
            pytest.skip("OPML文件不存在")

    def test_is_recent(self):
        """测试时间过滤"""
        fetcher = RSSFetcher()
        
        # 24小时内的文章
        from datetime import datetime, timedelta
        recent = (datetime.now() - timedelta(hours=12)).isoformat()
        assert fetcher._is_recent(recent) is True
        
        # 48小时外的文章
        old = (datetime.now() - timedelta(hours=72)).isoformat()
        assert fetcher._is_recent(old) is False

    def test_clean_html(self):
        """测试HTML清理"""
        fetcher = RSSFetcher()
        
        html = "<p>Hello <b>World</b></p>"
        clean = fetcher._clean_html(html)
        assert "<" not in clean
        assert "Hello World" in clean


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
