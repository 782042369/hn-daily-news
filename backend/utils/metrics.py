"""
指标收集模块
收集和记录系统运行指标
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import time
import json
from pathlib import Path


@dataclass
class Metric:
    """单个指标数据"""
    name: str
    value: float
    timestamp: float
    tags: Dict[str, str] = field(default_factory=dict)


class MetricsCollector:
    """指标收集器"""
    
    def __init__(self, storage_path: Optional[str] = None):
        self.metrics: List[Metric] = []
        self.storage_path = Path(storage_path) if storage_path else None
    
    def record(self, name: str, value: float, tags: Optional[Dict] = None):
        """记录指标"""
        metric = Metric(
            name=name,
            value=value,
            timestamp=time.time(),
            tags=tags or {}
        )
        self.metrics.append(metric)
    
    def record_duration(self, name: str, tags: Optional[Dict] = None):
        """记录操作耗时（返回finish函数）"""
        start_time = time.time()
        
        def finish():
            duration = time.time() - start_time
            self.record(f"{name}_duration", duration, tags)
            return duration
        
        return finish
    
    def get_metrics(self, name: Optional[str] = None) -> List[Metric]:
        """获取指标列表"""
        if name:
            return [m for m in self.metrics if m.name == name]
        return self.metrics
    
    def get_average(self, name: str) -> Optional[float]:
        """获取指标平均值"""
        metrics = self.get_metrics(name)
        if not metrics:
            return None
        return sum(m.value for m in metrics) / len(metrics)
    
    def save(self):
        """保存指标到文件"""
        if not self.storage_path:
            return
        
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        
        data = [
            {
                "name": m.name,
                "value": m.value,
                "timestamp": m.timestamp,
                "tags": m.tags
            }
            for m in self.metrics
        ]
        
        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def clear(self):
        """清空指标"""
        self.metrics.clear()


# 全局指标收集器
metrics = MetricsCollector()
