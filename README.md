# 📰 HN每日新闻简报

> 为程序员精选的每日技术热点 | 自动抓取 · AI摘要 · 每日更新

[![Daily Fetch](https://github.com/782042369/hn-daily-news/actions/workflows/daily-fetch.yml/badge.svg)](https://github.com/782042369/hn-daily-news/actions/workflows/daily-fetch.yml)
[![Deploy](https://github.com/782042369/hn-daily-news/actions/workflows/deploy.yml/badge.svg)](https://github.com/782042369/hn-daily-news/actions/workflows/deploy.yml)
[![Test](https://github.com/782042369/hn-daily-news/actions/workflows/test.yml/badge.svg)](https://github.com/782042369/hn-daily-news/actions/workflows/test.yml)

## 🌟 功能特性

- ✅ 每天北京时间8点自动抓取RSS源
- ✅ AI智能摘要（100-200字）
- ✅ 响应式设计，支持暗色模式
- ✅ 历史新闻浏览
- ✅ 自动部署到GitHub Pages

## 🏗️ 项目结构

```
hn-daily-news/
├── frontend/          # React前端
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── styles/
│   └── package.json
├── backend/           # Python后端
│   ├── app/
│   ├── tests/
│   ├── config/
│   └── requirements.txt
├── data/              # 数据存储
│   └── news/          # 每日新闻MD文件
├── docs/              # 文档
└── .github/workflows/ # CI/CD配置
```

## 🚀 快速开始

### 前端

```bash
cd frontend
npm install
npm run dev
```

### 后端

```bash
cd backend
pip install -r requirements.txt
python -m app.main
```

## 📋 RSS源配置

编辑 `backend/config/feeds.json` 添加或修改RSS源：

```json
[
  {
    "name": "源名称",
    "url": "https://example.com/rss"
  }
]
```

## ⚙️ 环境变量

创建 `backend/.env` 文件：

```env
OPENAI_API_KEY=your_api_key_here
```

## 🤖 自动化

项目使用GitHub Actions实现自动化：

- **daily-fetch.yml**: 每天北京时间8点自动抓取RSS
- **deploy.yml**: 推送到main分支时自动部署
- **test.yml**: 测试流水线

## 📜 License

MIT License

## 👥 贡献者

歪朝团队 - 六部协作

---

*Made with ❤️ by 歪朝开发团队*
