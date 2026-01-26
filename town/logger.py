'''
Author: clear.fang 729848336@qq.com
Date: 2026-01-26
Description: 模拟系统日志模块
'''

import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from model import SimulationState

class SimulationLogger:
    """模拟系统日志记录器"""
    
    def __init__(self, log_dir: str = "simulation_logs"):
        self.log_dir = log_dir
        self.txt_log_path = None
        self.json_log_path = None
        self._setup_logging()
    
    def _setup_logging(self):
        """设置日志系统"""
        # 创建日志目录
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        
        # 生成时间戳
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 设置日志文件路径
        self.txt_log_path = os.path.join(self.log_dir, f"simulation_{timestamp}.txt")
        self.json_log_path = os.path.join(self.log_dir, f"simulation_{timestamp}.json")
        
        # 初始化TXT日志文件
        with open(self.txt_log_path, "w", encoding="utf-8") as f:
            f.write(f"模拟系统日志 - 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*80 + "\n\n")
    
    def log_message(self, 
                   message: str, 
                   level: str = "INFO",
                   print_to_console: bool = True,
                   save_to_json: bool = False,
                   metadata: Optional[Dict[str, Any]] = None):
        """记录消息"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        formatted_message = f"[{timestamp}] [{level}] {message}"
        
        # 写入TXT文件
        with open(self.txt_log_path, "a", encoding="utf-8") as f:
            f.write(formatted_message + "\n")
        
        # 打印到控制台
        if print_to_console:
            print(formatted_message)
        
        # 保存到JSON文件（如果需要）
        if save_to_json and metadata:
            self._save_to_json(timestamp, level, message, metadata)
    
    def _save_to_json(self, timestamp: str, level: str, message: str, metadata: Dict[str, Any]):
        """保存到JSON日志文件"""
        log_entry = {
            "timestamp": timestamp,
            "level": level,
            "message": message,
            "metadata": metadata
        }
        
        # 读取现有日志或创建新的
        logs = []
        if os.path.exists(self.json_log_path):
            with open(self.json_log_path, "r", encoding="utf-8") as f:
                try:
                    logs = json.load(f)
                except:
                    logs = []
        
        # 添加新条目
        logs.append(log_entry)
        
        # 写回文件
        with open(self.json_log_path, "w", encoding="utf-8") as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)
    
    def log_agent_action(self, 
                        agent_id: str, 
                        action: str, 
                        action_params: Dict[str, Any],
                        stats: Dict[str, int],
                        world_snapshot: Dict[str, Any]):
        """记录智能体行动"""
        message = (f"{agent_id:8s} | 行动: {action:20s} | "
                  f"健康:{stats['health']:3d} 饥饿:{stats['hunger']:3d} "
                  f"心情:{stats['mood']:3d} 体力:{stats['stamina']:3d}")
        
        metadata = {
            "agent_id": agent_id,
            "action": action,
            "action_params": action_params,
            "stats": stats,
            "world_snapshot": world_snapshot
        }
        
        self.log_message(message, "ACTION", save_to_json=True, metadata=metadata)
    
    def log_world_event(self, event_type: str, description: str, details: Dict[str, Any]):
        """记录世界事件"""
        message = f"[世界事件] {description}"
        metadata = {
            "event_type": event_type,
            "description": description,
            "details": details
        }
        
        self.log_message(message, "WORLD", save_to_json=True, metadata=metadata)
    
    def log_simulation_summary(self, state: SimulationState):
        """记录模拟总结"""
        self.log_message("\n" + "="*60, "SUMMARY", print_to_console=False)
        self.log_message("模拟总结报告", "SUMMARY", print_to_console=False)
        self.log_message("="*60, "SUMMARY", print_to_console=False)
        
        # 分析数据
        diligent_logs = [log for log in state["logs"] if log["agent"] == "diligent"]
        lazy_logs = [log for log in state["logs"] if log["agent"] == "lazy"]
        
        self.log_message("\n【行为统计】", "SUMMARY", print_to_console=False)
        
        for agent_name, logs in [("勤奋型", diligent_logs), ("懒散型", lazy_logs)]:
            self.log_message(f"\n{agent_name}:", "SUMMARY", print_to_console=False)
            action_counts = {}
            for log in logs:
                action = log["action"]
                action_counts[action] = action_counts.get(action, 0) + 1
            
            for action, count in sorted(action_counts.items()):
                self.log_message(f"  {action:20s}: {count:3d}次", "SUMMARY", print_to_console=False)
        
        # 关键指标对比
        self.log_message("\n【关键指标对比】", "SUMMARY", print_to_console=False)
        self.log_message(f"{'指标':<10} | {'勤奋型':<10} | {'懒散型':<10} | {'差异'}", 
                        "SUMMARY", print_to_console=False)
        self.log_message("-" * 45, "SUMMARY", print_to_console=False)
        
        metrics = ["health", "hunger", "mood", "stamina"]
        for metric in metrics:
            diligent_vals = [log["stats"][metric] for log in diligent_logs if log["hour"] % 24 == 0]
            lazy_vals = [log["stats"][metric] for log in lazy_logs if log["hour"] % 24 == 0]
            
            d_avg = sum(diligent_vals)/len(diligent_vals) if diligent_vals else 0
            l_avg = sum(lazy_vals)/len(lazy_vals) if lazy_vals else 0
            
            self.log_message(f"{metric:<10} | {d_avg:>8.1f}  | {l_avg:>8.1f}  | {d_avg-l_avg:>+6.1f}", 
                           "SUMMARY", print_to_console=False)
    
    def get_log_paths(self) -> Dict[str, str]:
        """获取日志文件路径"""
        return {
            "txt_log": self.txt_log_path,
            "json_log": self.json_log_path
        }