"""
告警模块
发送告警通知
"""

import httpx
from typing import Optional, List
from datetime import datetime
import os


class FeishuAlerter:
    """飞书告警器"""
    
    def __init__(self, webhook_url: Optional[str] = None):
        self.webhook_url = webhook_url or os.getenv("FEISHU_WEBHOOK_URL")
    
    async def send_alert(
        self,
        title: str,
        message: str,
        level: str = "warning",  # info, warning, error, critical
        mention_users: Optional[List[str]] = None
    ):
        """发送飞书告警"""
        if not self.webhook_url:
            print(f"[Alert] {level.upper()}: {title} - {message}")
            return
        
        color_map = {
            "info": "blue",
            "warning": "yellow",
            "error": "red",
            "critical": "red"
        }
        
        elements = [
            {
                "tag": "div",
                "text": {"tag": "plain_text", "content": message}
            },
            {
                "tag": "div",
                "text": {
                    "tag": "plain_text",
                    "content": f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                }
            }
        ]
        
        # @相关人员
        if mention_users:
            elements.append({
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": " ".join(
                        [f"<at user_id='{uid}'>用户</at>" for uid in mention_users]
                    )
                }
            })
        
        payload = {
            "msg_type": "interactive",
            "card": {
                "config": {"wide_screen_mode": True},
                "header": {
                    "title": {
                        "tag": "plain_text",
                        "content": f"【{level.upper()}】{title}"
                    },
                    "template": color_map.get(level, "blue")
                },
                "elements": elements
            }
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(self.webhook_url, json=payload)
                if response.status_code != 200:
                    print(f"Failed to send alert: {response.text}")
        except Exception as e:
            print(f"Error sending alert: {e}")
    
    async def info(self, title: str, message: str, mention: Optional[List[str]] = None):
        """发送INFO级别告警"""
        await self.send_alert(title, message, "info", mention)
    
    async def warning(self, title: str, message: str, mention: Optional[List[str]] = None):
        """发送WARNING级别告警"""
        await self.send_alert(title, message, "warning", mention)
    
    async def error(self, title: str, message: str, mention: Optional[List[str]] = None):
        """发送ERROR级别告警"""
        await self.send_alert(title, message, "error", mention)
    
    async def critical(self, title: str, message: str, mention: Optional[List[str]] = None):
        """发送CRITICAL级别告警"""
        await self.send_alert(title, message, "critical", mention)


# 全局告警器
alerter = FeishuAlerter()
