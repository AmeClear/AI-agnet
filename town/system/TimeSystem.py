'''
Author: clear.fang 729848336@qq.com
Date: 2026-01-30 17:18:52
LastEditors: clear.fang 729848336@qq.com
LastEditTime: 2026-01-30 18:29:06
FilePath: \AI-agnet\town\system\TimeSystem.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from model.TownWorld import TownWorld

def update_time(world:TownWorld):
    world.update_time(1)
    #智能体行为
    check_action()
    check_agent_thinking()

def check_action(world:TownWorld):
    "处理智能体行为"
    for agent in world.agents.values():
        agent.action[0].cost_action(agent)

def check_agent_thinking(world:TownWorld):
    "智能体思考"
    for agent in world.agents.values():
        agent.decide()

