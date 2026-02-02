from __future__ import annotations  # 放在文件最顶部
from typing import TYPE_CHECKING

# 只在类型检查时导入
if TYPE_CHECKING:
    from TownAgent import TownAgent
    from TownWorld import TownWorld,TownFood
    from ImpactEffect import ImpactHunger, ImpactMood, ImpactStam
from town.system.ActionSystem import make_food
from system.HealthSystem import check_agent_action, check_agent_health
class TownAction:
    _stamina_cost:int =0#体力消耗每小时
    _hunger_cost:int=0#饥饿消耗每小时
    _hour_cost:int = 0#目标行动时间
    __progress:int =0 #行动实时进度
    def push_action(self,agent:TownAgent,world:TownWorld,hour: int) -> int:
        "行动添加"
        self._hour_cost = hour
        #体力不够，饥饿值不够，有行动占用，健康值不足
        if check_agent_action(agent,self._stamina_cost,self._hunger_cost,hour) or check_agent_health(agent)<0:
            return -1
        #占用行为
        agent.action.append(self)
        return 1
    
    def do_action(self,agent:TownAgent,world:TownWorld,hour: int):
        "执行"
        ImpactHunger().impact(agent,self._hunger_cost*hour)
        ImpactStam().impact(agent,self._stamina_cost*hour)
    
    def cost_action(self,agent:TownAgent):
        "行动推进"
        self.__progress+=1
        if self.__progress == self._hour_cost:
            self.do_action()
            agent.action.remove()
        

class Work(TownAction):
    "工作"
    def __init__(self) -> None:
        self._stamina_cost=20
        self._hunger_cost=10


class Rect(TownAction):
    "休息"
    def __init__(self) -> None:
        self._stamina_cost=-10
        self._hunger_cost=15

class MakeFood(Work):
    "做饭"
    def __init__(self) -> None:
        super().__init__()
    def push_action(self, agent: TownAgent, world: TownWorld, hour: int) -> int:
        #食物不够
        if world.meat+world.vegetables<3:
            return -1
        return super().push_action(agent, world, hour)
        
    def do_action(self, agent: TownAgent, world: TownWorld, hour: int):
        #智能体食物制作
        food = make_food(world)
        world.food[food]+=1
        ImpactHunger().impact(agent,self._hunger_cost*hour)
        ImpactStam().impact(agent,self._stamina_cost*hour)
        #占用行为
        agent.action.append(self)
        return 1

class Eat(TownAction):
    "进食"
    food:TownFood
    def __init__(self,food) -> None:
        self.food = food

    def do_action(self, agent: TownAgent, world: TownWorld, hour: int):
        ImpactHunger().impact(agent,self.food.hunger)
        ImpactMood().impact(agent,self.food.mood)
        ImpactStam().impact(agent,self.food.stamina)
        
    def push_action(self, agent: TownAgent, world: TownWorld, hour: int) -> int:
        if world.food[self.food]==0:
            return -1
        return super().push_action(agent, world, hour)
    
class Plant(TownAction):
    "种植"
    def __init__(self):
        super().__init__()
    def do_action(self, agent, world, hour):
        super().do_action(agent, world, hour)
        world.vegetables+=1

class Feed(TownAction):
    "饲养"
    def __init__(self):
        super().__init__()
    def do_action(self, agent, world, hour):
        super().do_action(agent, world, hour)
        world.meat+=1

