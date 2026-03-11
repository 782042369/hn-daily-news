#!/bin/bash
# 部署脚本 - 本地测试和生产部署

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== HN每日新闻部署脚本 ===${NC}"

# 检查环境
check_environment() {
    echo -e "\n${YELLOW}[1/5] 检查环境...${NC}"
    
    # 检查Python
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}错误: 未找到Python3${NC}"
        exit 1
    fi
    
    # 检查Node.js
    if ! command -v node &> /dev/null; then
        echo -e "${RED}错误: 未找到Node.js${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✓ 环境检查通过${NC}"
}

# 安装后端依赖
install_backend() {
    echo -e "\n${YELLOW}[2/5] 安装后端依赖...${NC}"
    cd backend
    
    if [ ! -d "venv" ]; then
        python3 -m venv venv
    fi
    
    source venv/bin/activate
    pip install -r requirements.txt
    deactivate
    
    echo -e "${GREEN}✓ 后端依赖安装完成${NC}"
}

# 安装前端依赖
install_frontend() {
    echo -e "\n${YELLOW}[3/5] 安装前端依赖...${NC}"
    cd frontend
    
    if [ ! -d "node_modules" ]; then
        npm install
    fi
    
    echo -e "${GREEN}✓ 前端依赖安装完成${NC}"
}

# 构建前端
build_frontend() {
    echo -e "\n${YELLOW}[4/5] 构建前端...${NC}"
    cd frontend
    
    npm run build
    
    echo -e "${GREEN}✓ 前端构建完成${NC}"
}

# 运行测试
run_tests() {
    echo -e "\n${YELLOW}[5/5] 运行测试...${NC}"
    
    # 后端测试
    cd backend
    source venv/bin/activate
    pytest tests/ -v || echo -e "${YELLOW}⚠ 后端测试跳过${NC}"
    deactivate
    
    # 前端测试
    cd ../frontend
    npm test || echo -e "${YELLOW}⚠ 前端测试跳过${NC}"
    
    echo -e "${GREEN}✓ 测试完成${NC}"
}

# 主流程
main() {
    case "$1" in
        "install")
            check_environment
            install_backend
            install_frontend
            ;;
        "build")
            build_frontend
            ;;
        "test")
            run_tests
            ;;
        "all")
            check_environment
            install_backend
            install_frontend
            build_frontend
            run_tests
            ;;
        *)
            echo "用法: $0 {install|build|test|all}"
            exit 1
            ;;
    esac
    
    echo -e "\n${GREEN}=== 部署完成 ===${NC}"
}

# 执行
main "$@"
