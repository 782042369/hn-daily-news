# HN 每日新闻推送系统

> 每天北京时间8点自动抓取 Hacker News 博客，生成AI简报推送到GitHub

## 📖 项目简介

本项目是一个RSS订阅聚合系统，每天自动抓取Hacker News相关博客内容，通过AI生成100-200字简报，推送到GitHub Pages供程序员阅读。

## 🎯 核心功能

- ✅ RSS订阅聚合（基于HN popular blogs）
- ✅ 每天北京时间8点自动抓取
- ✅ AI生成100-200字简报
- ✅ 自动推送到GitHub
- ✅ 前端渲染Markdown
- ✅ 按日期分类浏览

## 🛠️ 技术栈

- **前端：** React 18+
- **后端：** Python 3.9+
- **部署：** GitHub Actions + GitHub Pages
- **AI：** OpenAI API / Claude API

## 📁 项目结构

```
hn-daily-news/
├── backend/              # Python后端
│   ├── rss_fetcher.py   # RSS抓取
│   ├── ai_summarizer.py # AI总结
│   ├── scheduler.py     # 定时任务
│   └── data/            # 数据存储
│       └── news/
│           ├── 2026-03-11.md
│           └── 2026-03-11.json
├── frontend/            # React前端
│   ├── src/
│   ├── public/
│   └── package.json
├── .github/
│   └── workflows/
│       └── daily-fetch.yml
└── README.md
```

## 🚀 快速开始

### 后端

```bash
cd backend
pip install -r requirements.txt
python scheduler.py
```

### 前端

```bash
cd frontend
npm install
npm start
```

## 📋 功能清单

- [ ] RSS抓取服务
- [ ] AI内容总结
- [ ] 数据管理
- [ ] 前端展示
- [ ] 自动化部署

## 📝 Git提交规范

**格式：** `<type>(<scope>): <subject>`

**Type类型：**
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式
- `refactor`: 重构
- `test`: 测试
- `chore`: 构建/工具
- `perf`: 性能优化

**示例：**
```bash
git add backend/rss_fetcher.py
git commit -m "feat(rss): 添加RSS抓取模块"
git push origin main
```

## 📚 文档

- [需求清单](docs/requirements.md)
- [API文档](docs/api.md)
- [部署指南](docs/deployment.md)
- [成本分析](docs/cost-analysis.md)

## 🤝 贡献指南

1. Fork本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'feat: 添加某个功能'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交Pull Request

## 📄 开源协议

MIT License

## 👥 团队

**歪朝会议第一次项目组**

- **兵部** - 后端开发
- **工部** - 前端开发 & 部署
- **户部** - 数据管理
- **吏部** - 项目管理
- **刑部** - 质量保障
- **礼部** - 协调 & 文档

## 📞 联系方式

项目链接: [https://github.com/782042369/hn-daily-news](https://github.com/782042369/hn-daily-news)

---

**最后更新：** 2026-03-11
**项目代号：** 歪朝会议第一次
