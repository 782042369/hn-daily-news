"""
健康检查模块
提供系统健康状态检查端点
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import Dict, Any
import psutil
import httpx

router = APIRouter()


@router.get("/health")
async def health_check():
    """基础健康检查"""
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
        "memory": check_memory(),
        "last_fetch": get_last_fetch_time()
    }
    
    all_healthy = all(c["status"] == "ok" for c in checks.values())
    
    return {
        "status": "healthy" if all_healthy else "degraded",
        "timestamp": datetime.utcnow().isoformat(),
        "checks": checks
    }


async def check_rss_feeds() -> Dict[str, Any]:
    """检查RSS源可用性"""
    try:
        # 测试抓取一个RSS源
        test_url = "https://hnrss.org/frontpage"
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(test_url)
            if response.status_code == 200:
                return {
                    "status": "ok",
                    "message": "RSS feeds accessible"
                }
    except Exception as e:
        return {
            "status": "error",
            "message": f"RSS check failed: {str(e)}"
        }


async def check_openai_api() -> Dict[str, Any]:
    """检查OpenAI API可用性"""
    import os
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        return {
            "status": "warning",
            "message": "OpenAI API key not configured"
        }
    
    try:
        # 简单的API连通性测试（不实际调用）
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                "https://api.openai.com/v1/models",
                headers={"Authorization": f"Bearer {api_key}"}
            )
            if response.status_code == 200:
                return {
                    "status": "ok",
                    "message": "OpenAI API accessible"
                }
    except Exception as e:
        return {
            "status": "error",
            "message": f"OpenAI API check failed: {str(e)}"
        }


def check_disk_space() -> Dict[str, Any]:
    """检查磁盘空间"""
    try:
        disk = psutil.disk_usage('/')
        free_gb = disk.free / (1024 ** 3)
        percent_used = disk.percent
        
        if free_gb < 10:
            return {
                "status": "warning",
                "message": f"Low disk space: {free_gb:.2f}GB free",
                "free_gb": round(free_gb, 2),
                "percent_used": percent_used
            }
        
        return {
            "status": "ok",
            "message": f"Disk space OK: {free_gb:.2f}GB free",
            "free_gb": round(free_gb, 2),
            "percent_used": percent_used
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Disk check failed: {str(e)}"
        }


def check_memory() -> Dict[str, Any]:
    """检查内存使用"""
    try:
        memory = psutil.virtual_memory()
        percent_used = memory.percent
        
        if percent_used > 80:
            return {
                "status": "warning",
                "message": f"High memory usage: {percent_used}%",
                "percent_used": percent_used
            }
        
        return {
            "status": "ok",
            "message": f"Memory usage OK: {percent_used}%",
            "percent_used": percent_used
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Memory check failed: {str(e)}"
        }


def get_last_fetch_time() -> Dict[str, Any]:
    """获取最后一次抓取时间"""
    from pathlib import Path
    import json
    
    state_file = Path(__file__).parent.parent / "data" / "state.json"
    
    if not state_file.exists():
        return {
            "status": "warning",
            "message": "No fetch history found"
        }
    
    try:
        with open(state_file, 'r') as f:
            state = json.load(f)
            last_fetch = state.get("lastFetch")
            
            if last_fetch:
                return {
                    "status": "ok",
                    "message": f"Last fetch: {last_fetch}",
                    "last_fetch": last_fetch
                }
            else:
                return {
                    "status": "warning",
                    "message": "No last fetch time recorded"
                }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to read state: {str(e)}"
        }
