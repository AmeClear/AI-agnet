'''
Author: clear.fang 729848336@qq.com
Date: 2026-02-02 14:01:46
LastEditors: clear.fang 729848336@qq.com
LastEditTime: 2026-02-25 21:08:00
FilePath: \AI-agnet\town\main.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''

from model.ObjectDefine import TownAgent,TownWorld
from agent.llm import deepseek
from system.TimeSystem import update_time
if __name__ == "__main__":
    world = TownWorld()
    world.meat = 10
    world.vegetables = 10
    agent1 = TownAgent("Adam", "diligent")
    agent1.set_llm(deepseek)
    world.agents.update({"Adam":agent1})
    hour =0
    while(hour < 1):
        hour +=1
        update_time(world)
