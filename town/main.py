
from model.ObjectDefine import TownAgent,TownWorld
from agent.llm import deepseek
from system.TimeSystem import update_time
if __name__ == "__main__":
    world = TownWorld()
    agent1 = TownAgent("Adam", "diligent")
    agent1.set_llm(deepseek)
    world.agents.update({"Adam":agent1})
    hour =0
    while(hour < 1):
        hour +=1
        update_time(world)
