'''
Author: clear.fang 729848336@qq.com
Date: 2026-01-26 17:33:42
LastEditors: clear.fang 729848336@qq.com
LastEditTime: 2026-01-26 22:22:09
FilePath: \AI-agnet\town\agent_work_graph.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from model import AgentState,WorldState,SimulationState
import random
from agent_thinking import ai_evaluate_meal

# 新增：异步版本的 decide_and_act
async def decide_and_act(state: SimulationState, agent_id: str) -> AgentState:
    """决定并执行一个智能体一小时的动作（异步修复版）"""
    agent = state[agent_id].copy()
    world = state["world"]
    hour = world["current_hour"]
    is_daytime = 6 <= hour < 18
    is_night = not is_daytime
    
    # 基础消耗（时间流逝）
    agent["hunger"] = min(100, agent["hunger"] + 5)
    
    # 1. 强制优先级决策
    # 饥饿超过70且有食材 -> 做饭吃饭
    if agent["hunger"] >= 70 and world["vegetables"] + world["meat"] >= 3:
        return await _cook_and_eat(agent, world)
    
    # 体力过低 -> 休息
    if agent["stamina"] < 20:
        return _rest(agent, world)
    
    # 夜晚睡觉时间
    if hour >= 22 or hour < 6:
        return _sleep(agent, world)
    
    # 2. 策略决策（基于倾向性）
    rand = random.random()
    bias = agent["labour_bias"] if is_daytime else agent["rest_bias"] * 0.5
    
    if is_daytime:
        # 白天劳动决策
        if rand < bias * 0.4 and world["vegetables"] < 8:
            return _plant_crops(agent, world)
        elif rand < bias * 0.7 and world["meat"] < 8:
            return _raise_animals(agent, world)
        elif rand < bias and world["planted_crops"]:
            return _harvest_crops(agent, world)
        elif rand < bias + 0.1 and world["raising_animals"]:
            return _slaughter_animals(agent, world)
        else:
            return _rest(agent, world)
    else:
        # 夜晚决策
        if agent["hunger"] > 80 and world["vegetables"] + world["meat"] >= 3:
            return await _cook_and_eat(agent, world)
        return _rest(agent, world)

# ==================== 3. 具体行动函数 ====================
async def _cook_and_eat(agent: AgentState, world: WorldState) -> AgentState:
    if world["vegetables"] + world["meat"] < 3:
        return agent
    
    # 消耗食材
    ratio = random.choice([(2,1), (1,2), (1,1)])
    veg_needed = 3 * ratio[0] // sum(ratio)
    meat_needed = 3 - veg_needed
    
    # 【核心升级】调用AI评定
    evaluation = await ai_evaluate_meal(
        ingredients={"veg": veg_needed, "meat": meat_needed},
        agent_mood=agent["mood"]
    )
    
    # 使用AI评定的数值
    agent["hunger"] = max(0, agent["hunger"] - evaluation["satiation"])
    agent["mood"] = min(100, agent["mood"] + evaluation["deliciousness"])
    agent["last_action"] = f"cook_and_eat: {evaluation['description']}"
    
    # 记录消耗的食材
    agent["last_action_params"] = {
        "veg_used": veg_needed,
        "meat_used": meat_needed,
        "evaluation": evaluation
    }
    
    world["vegetables"] -= veg_needed
    world["meat"] -= meat_needed
    
    return agent

# ... 其他函数保持不变 ...
def _plant_crops(agent: AgentState, world: WorldState) -> AgentState:
    """种植作物"""
    if agent["stamina"] < 20:
        return _rest(agent, world)
    
    # 消耗体力
    stamina_cost = 40  # 2小时劳动
    if world["current_hour"] < 6 or world["current_hour"] >= 18:
        stamina_cost += 5  # 夜晚额外消耗
    
    agent["stamina"] = max(0, agent["stamina"] - stamina_cost)
    agent["mood"] = max(0, agent["mood"] - random.randint(10, 30))
    agent["last_action"] = "plant_crops"
    agent["last_action_params"] = {
        "stamina_cost": stamina_cost,
        "mood_cost": random.randint(10, 30)
    }
    
    return agent

def _rest(agent: AgentState, world: WorldState) -> AgentState:
    """休息"""
    rest_type = random.choice(["read", "game", "sing"])
    mood_boost = random.randint(10, 30)
    
    agent["stamina"] = min(100, agent["stamina"] + 5)
    agent["mood"] = min(100, agent["mood"] + mood_boost)
    agent["last_action"] = f"rest_{rest_type}"
    agent["last_action_params"] = {
        "type": rest_type,
        "mood_boost": mood_boost
    }
    
    return agent

def _sleep(agent: AgentState, world: WorldState) -> AgentState:
    """睡觉"""
    stamina_recovery = 10  # 每小时恢复
    if world["current_hour"] < 6 or world["current_hour"] >= 18:
        stamina_recovery += 5  # 夜晚额外恢复
    
    agent["stamina"] = min(100, agent["stamina"] + stamina_recovery)
    agent["last_action"] = "sleep"
    agent["last_action_params"] = {"stamina_recovery": stamina_recovery}
    
    return agent

def _raise_animals(agent: AgentState, world: WorldState) -> AgentState:
    """饲养动物"""
    agent["stamina"] = max(0, agent["stamina"] - 40)
    agent["mood"] = max(0, agent["mood"] - random.randint(10, 30))
    agent["last_action"] = "raise_animals"
    agent["last_action_params"] = {"stamina_cost": 40}
    return agent

def _harvest_crops(agent: AgentState, world: WorldState) -> AgentState:
    """收获作物"""
    agent["stamina"] = max(0, agent["stamina"] - 20)
    agent["last_action"] = "harvest_crops"
    agent["last_action_params"] = {"stamina_cost": 20}
    return agent

def _slaughter_animals(agent: AgentState, world: WorldState) -> AgentState:
    """屠宰动物"""
    agent["stamina"] = max(0, agent["stamina"] - 20)
    agent["mood"] = max(0, agent["mood"] - random.randint(10, 30))
    agent["last_action"] = "slaughter_animals"
    agent["last_action_params"] = {"stamina_cost": 20}
    return agent