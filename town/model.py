'''
Author: clear.fang 729848336@qq.com
Date: 2026-01-26 17:31:43
LastEditors: clear.fang 729848336@qq.com
LastEditTime: 2026-01-26 17:33:17
FilePath: \AI-agnet\town\model.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from typing import TypedDict, List, Dict, Any, Literal

class WorldState(TypedDict):
    """世界共享状态"""
    current_hour: int  # 0 到 (7*24-1)
    vegetables: int    # 素食食材（吨）
    meat: int          # 肉类食材（吨）
    planted_crops: Dict[str, Dict]  # 种植中的作物
    raising_animals: Dict[str, Dict] # 饲养中的动物

class AgentState(TypedDict):
    """智能体个人状态"""
    agent_id: str
    agent_type: Literal["diligent", "lazy"]
    
    # 核心数值（0-100）
    health: int
    hunger: int
    mood: int
    stamina: int
    
    # 行为倾向
    labour_bias: float
    rest_bias: float
    
    # 状态标记
    location: Literal["home", "field", "barn"]
    last_action: str
    last_action_params: Dict[str, Any]

class SimulationState(TypedDict):
    """模拟整体状态"""
    world: WorldState
    diligent: AgentState
    lazy: AgentState
    logs: List[Dict]