# main.py
from typing import Literal
from model import TownAgent, TownWorld
from system.TimeSystem import update_time

# 使用你的类和函数
if __name__ == "__main__":
    world = TownWorld()
    agent1 = TownAgent("Adam", "diligent")
    world.agents.update({"Adam":agent1})
    hour =0
    while(hour < 24):
        hour +=1
        update_time(world)