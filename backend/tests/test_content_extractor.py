"""
单元测试 - 内容提取模块
"""
import pytest
from modules.content_extractor import ContentExtractor


class TestContentExtractor:
    """内容提取器测试"""

    def test_extract_main_content(self):
        """测试正文提取"""
        extractor = ContentExtractor()
        
        html = """
        <html>
        <body>
            <nav>导航栏</nav>
            <article>
                <p>这是第一段内容，长度足够超过50个字符，这样可以被保留下来作为有效内容。</p>
                <p>这是第二段内容，同样长度足够，应该也会被保留。</p>
            </article>
            <footer>页脚</footer>
        </body>
        </html>
        """
        
        content = extractor._extract_main_content(html)
        assert "第一段内容" in content
        assert "导航栏" not in content
        assert "页脚" not in content

    def test_content_length_limit(self):
        """测试内容长度限制"""
        extractor = ContentExtractor()
        
        # 生成超长内容
        long_html = f"<article><p>{'A' * 5000}</p></article>"
        content = extractor._extract_main_content(long_html)
        
        assert len(content) <= 2000


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
