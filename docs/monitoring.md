# 监控告警系统设计

## 概述

本文档描述HN每日新闻系统的监控和告警架构，确保系统稳定运行和快速故障响应。

## 1. 日志系统架构

### 1.1 日志分级

| 级别 | 用途 | 示例 |
|------|------|------|
| DEBUG | 开发调试 | 变量值、函数调用 |
| INFO | 正常运行 | RSS抓取开始/完成 |
| WARNING | 潜在问题 | 某个RSS源超时 |
| ERROR | 错误但可恢复 | API调用失败 |
| CRITICAL | 严重错误 | 系统崩溃、数据丢失 |

### 1.2 日志格式

```python
# backend/utils/logger.py
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
            
        return json.dumps(log_data)
```

### 1.3 日志存储

- **本地文件**: `/var/log/hn-daily-news/`
- **轮转策略**: 按天轮转，保留30天
- **GitHub Actions日志**: 自动保留90天

## 2. 监控指标

### 2.1 系统指标

| 指标 | 阈值 | 告警级别 |
|------|------|----------|
| RSS抓取成功率 | < 80% | WARNING |
| API响应时间 | > 5s | WARNING |
| 内存使用 | > 80% | WARNING |
| 磁盘空间 | < 10GB | CRITICAL |

### 2.2 业务指标

| 指标 | 正常范围 | 说明 |
|------|----------|------|
| 每日文章数 | 20-50篇 | 少于20可能RSS源异常 |
| 摘要生成成功率 | > 95% | OpenAI API调用成功率 |
| 页面加载时间 | < 3s | 用户体验指标 |

### 2.3 指标收集

```python
# backend/utils/metrics.py
from dataclasses import dataclass
from typing import Dict
import time

@dataclass
class Metric:
    name: str
    value: float
    timestamp: float
    tags: Dict[str, str]

class MetricsCollector:
    def __init__(self):
        self.metrics = []
    
    def record(self, name: str, value: float, tags: Dict = None):
        metric = Metric(
            name=name,
            value=value,
            timestamp=time.time(),
            tags=tags or {}
        )
        self.metrics.append(metric)
        
    def record_duration(self, name: str, tags: Dict = None):
        """记录操作耗时"""
        start_time = time.time()
        def finish():
            duration = time.time() - start_time
            self.record(f"{name}_duration", duration, tags)
        return finish
```

## 3. 告警机制

### 3.1 告警渠道

| 渠道 | 用途 | 响应时间 |
|------|------|----------|
| 飞书群消息 | 实时告警 | < 1分钟 |
| GitHub Issues | 问题跟踪 | < 1小时 |
| 邮件 | 备用通知 | < 5分钟 |

### 3.2 飞书告警机器人

```python
# backend/utils/alerts.py
import httpx
from typing import Optional

class FeishuAlerter:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
    
    async def send_alert(
        self,
        title: str,
        message: str,
        level: str = "warning",  # info, warning, error, critical
        mention_users: Optional[list] = None
    ):
        """发送飞书告警"""
        color_map = {
            "info": "blue",
            "warning": "yellow",
            "error": "red",
            "critical": "red"
        }
        
        payload = {
            "msg_type": "interactive",
            "card": {
                "config": {"wide_screen_mode": True},
                "header": {
                    "title": {"tag": "plain_text", "content": f"【{level.upper()}】{title}"},
                    "template": color_map.get(level, "blue")
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {"tag": "plain_text", "content": message}
                    },
                    {
                        "tag": "div",
                        "text": {"tag": "plain_text", "content": f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"}
                    }
                ]
            }
        }
        
        # @相关人员
        if mention_users:
            payload["card"]["elements"].append({
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": " ".join([f"<at user_id='{uid}'>用户</at>" for uid in mention_users])
                }
            })
        
        async with httpx.AsyncClient() as client:
            await client.post(self.webhook_url, json=payload)
```

### 3.3 告警规则

```yaml
# 告警规则配置
alerts:
  - name: rss_fetch_failure
    condition: "success_rate < 0.8"
    severity: warning
    message: "RSS抓取成功率低于80%"
    channels: [feishu]
    
  - name: api_timeout
    condition: "response_time > 5000"
    severity: warning
    message: "API响应时间超过5秒"
    channels: [feishu]
    
  - name: daily_fetch_failed
    condition: "job_status == 'failed'"
    severity: critical
    message: "每日抓取任务失败"
    channels: [feishu, email]
    mention: ["ou_98221b1bc0f2ecdc5b431273381daf77"]  # @杨宏旋
```

## 4. 健康检查

### 4.1 后端健康检查

```python
# backend/app/health.py
from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/health")
async def health_check():
    """健康检查端点"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

@router.get("/health/detailed")
async def detailed_health():
    """详细健康检查"""
    checks = {
        "rss_feeds": await check_rss_feeds(),
        "openai_api": await check_openai_api(),
        "disk_space": check_disk_space(),
        "last_fetch": get_last_fetch_time()
    }
    
    all_healthy = all(c["status"] == "ok" for c in checks.values())
    
    return {
        "status": "healthy" if all_healthy else "degraded",
        "checks": checks
    }
```

### 4.2 GitHub Actions健康检查

```yaml
# .github/workflows/health-check.yml
name: Health Check

on:
  schedule:
    - cron: '0 */6 * * *'  # 每6小时检查一次

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - name: Check website
        run: |
          response=$(curl -s -o /dev/null -w "%{http_code}" https://782042369.github.io/hn-daily-news/)
          if [ $response -ne 200 ]; then
            echo "::error::Website returned $response"
            exit 1
          fi
```

## 5. 故障处理流程

### 5.1 故障分级

| 级别 | 定义 | 响应时间 | 处理时间 |
|------|------|----------|----------|
| P0 | 系统完全不可用 | < 5分钟 | < 30分钟 |
| P1 | 核心功能受影响 | < 15分钟 | < 2小时 |
| P2 | 部分功能异常 | < 1小时 | < 1天 |
| P3 | 小问题，不影响使用 | < 4小时 | < 1周 |

### 5.2 处理流程

```
故障发现 → 告警通知 → 初步评估 → 故障分级 → 应急响应 → 问题修复 → 复盘总结
```

### 5.3 故障复盘模板

```markdown
# 故障复盘报告

## 基本信息
- 故障时间：YYYY-MM-DD HH:MM - HH:MM
- 故障级别：P0/P1/P2/P3
- 影响范围：
- 处理人员：

## 时间线
- HH:MM 发现问题
- HH:MM 告警通知
- HH:MM 开始排查
- HH:MM 定位原因
- HH:MM 修复完成

## 根本原因
[详细描述]

## 修复方案
[详细描述]

## 预防措施
- [ ] 措施1
- [ ] 措施2

## 经验教训
[总结]
```

## 6. 监控仪表板

### 6.1 关键指标看板

```
┌─────────────────────────────────────────┐
│  HN每日新闻监控看板                      │
├─────────────────────────────────────────┤
│  RSS抓取成功率: ████████░░ 85%         │
│  今日文章数: 32篇                        │
│  API平均响应: 1.2s                       │
│  最后更新: 2026-03-11 08:00             │
├─────────────────────────────────────────┤
│  最近告警:                               │
│  ⚠️  10:23 - RSS源超时 (已恢复)         │
│  ✅ 09:15 - 每日抓取完成                 │
└─────────────────────────────────────────┘
```

### 6.2 实现方式

- **方案A**: GitHub Actions日志 + 飞书告警（推荐，简单）
- **方案B**: Grafana + Prometheus（复杂，需要独立服务器）
- **方案C**: 自建监控页面（中等复杂度）

## 7. 实施计划

### Phase 1: 基础监控（本周）
- [ ] 日志系统（Python logging）
- [ ] 健康检查端点
- [ ] 飞书告警机器人

### Phase 2: 增强监控（下周）
- [ ] 指标收集系统
- [ ] 告警规则配置
- [ ] 故障处理流程

### Phase 3: 监控仪表板（第三周）
- [ ] 监控页面开发
- [ ] 历史数据可视化
- [ ] 告警统计报表

---

*文档版本: v1.0*  
*创建时间: 2026-03-11*  
*负责人: 工部*
