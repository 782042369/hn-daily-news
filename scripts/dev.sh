#!/bin/bash
# 本地开发环境启动脚本

set -e

echo "🚀 启动HN每日新闻开发环境..."

# 启动后端
echo "📡 启动后端服务..."
cd backend
source venv/bin/activate 2>/dev/null || python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt > /dev/null 2>&1
uvicorn app.main:app --reload --port 8000 &
BACKEND_PID=$!
cd ..

# 等待后端启动
sleep 3

# 启动前端
echo "🎨 启动前端服务..."
cd frontend
npm install > /dev/null 2>&1
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ 开发环境已启动！"
echo ""
echo "📡 后端: http://localhost:8000"
echo "🎨 前端: http://localhost:5173"
echo ""
echo "按 Ctrl+C 停止所有服务"

# 等待用户中断
trap "echo ''; echo '🛑 停止服务...'; kill $BACKEND_PID $FRONTEND_PID; exit 0" INT

wait
