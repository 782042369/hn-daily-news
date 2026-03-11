# 部署文档

## 架构概览

```
┌─────────────────┐
│  GitHub Actions │
│  (定时任务)      │
└────────┬────────┘
         │ 每天8:00 UTC+8
         ▼
┌─────────────────┐
│  Python后端     │
│  - RSS抓取      │
│  - 内容提取     │
│  - AI摘要       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Markdown文件   │
│  data/news/     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  React前端      │
│  GitHub Pages   │
└─────────────────┘
```

## 部署步骤

### 1. Fork仓库

点击右上角Fork按钮

### 2. 配置Secrets

在仓库设置中添加以下Secrets：

- `OPENAI_API_KEY`: OpenAI API密钥

### 3. 启用GitHub Pages

1. 进入仓库Settings > Pages
2. Source选择"GitHub Actions"
3. 等待部署完成

### 4. 访问网站

```
https://<username>.github.io/hn-daily-news/
```

## 本地开发

### 前端

```bash
cd frontend
npm install
npm run dev
# 访问 http://localhost:5173
```

### 后端

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
cp .env.example .env
# 编辑 .env 填入API密钥
python -m app.main
```

## 监控与告警

### 日志查看

GitHub Actions > daily-fetch > 查看运行日志

### 失败通知

配置GitHub Actions通知：
1. 个人设置 > Notifications
2. 启用Actions通知

## 成本估算

- OpenAI API: ~$0.45/天 (20篇文章)
- GitHub Actions: 免费 (公开仓库)
- GitHub Pages: 免费

## 故障排查

### RSS抓取失败

- 检查网络连接
- 验证RSS URL有效性
- 查看Actions日志

### 部署失败

- 检查package.json依赖
- 验证构建配置
- 查看Actions日志

### 前端无法加载数据

- 检查GitHub Pages是否启用
- 验证数据文件路径
- 检查CORS配置
