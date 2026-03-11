#!/bin/bash
# 数据迁移脚本 - 从旧demo迁移到新项目

set -e

OLD_DEMO="/root/clawd/scripts/hn-blogs-rss"
NEW_PROJECT="/root/hn-daily-news"

echo "📦 数据迁移脚本"
echo "从: $OLD_DEMO"
echo "到: $NEW_PROJECT"
echo ""

# 检查源目录
if [ ! -d "$OLD_DEMO" ]; then
    echo "❌ 源目录不存在: $OLD_DEMO"
    exit 1
fi

# 迁移OPML文件
echo "📋 迁移OPML文件..."
if [ -f "$OLD_DEMO/opml.xml" ]; then
    cp "$OLD_DEMO/opml.xml" "$NEW_PROJECT/backend/config/"
    echo "✓ opml.xml已迁移"
fi

# 迁移历史数据
echo "📊 迁移历史数据..."
if [ -d "$OLD_DEMO/data" ]; then
    mkdir -p "$NEW_PROJECT/data"
    cp -r "$OLD_DEMO/data"/* "$NEW_PROJECT/data/" 2>/dev/null || echo "⚠ 无历史数据"
    echo "✓ 历史数据已迁移"
fi

# 迁移状态文件
echo "💾 迁移状态文件..."
if [ -f "$OLD_DEMO/data/sent-articles.json" ]; then
    cp "$OLD_DEMO/data/sent-articles.json" "$NEW_PROJECT/data/state.json"
    echo "✓ 状态文件已迁移"
fi

# 从OPML提取RSS源
echo ""
echo "📝 从OPML提取RSS源配置..."
python3 << 'EOF'
import xml.etree.ElementTree as ET
import json

opml_file = "/root/hn-daily-news/backend/config/opml.xml"
output_file = "/root/hn-daily-news/backend/config/feeds.json"

try:
    tree = ET.parse(opml_file)
    root = tree.getroot()
    
    feeds = []
    for outline in root.findall(".//outline[@xmlUrl]"):
        name = outline.get('text', 'Unknown')
        url = outline.get('xmlUrl')
        if url:
            feeds.append({"name": name, "url": url})
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(feeds, f, indent=2, ensure_ascii=False)
    
    print(f"✓ 提取了 {len(feeds)} 个RSS源")
except Exception as e:
    print(f"⚠ 提取失败: {e}")
EOF

echo ""
echo "✅ 迁移完成！"
echo ""
echo "迁移的文件："
echo "  - backend/config/opml.xml"
echo "  - backend/config/feeds.json"
echo "  - data/ (历史数据)"
