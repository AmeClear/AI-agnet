from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional
from typing import Literal

from agent.OutPuts.PydanticPareser import pydantic_output
from agent.Prompts.StructOutputPrompt import struct_output_prompt
from agent.Prompts.TownObjectPrompt import make_food_prompt



class TownFood(BaseModel):
    "食物"
    name:str = Field(description="食物的名称")#名称
    hunger: Optional[int] = Field(
        default=None, description="食物的饱腹感，从 1 到 10"
    )#饥饿值
    mood: Optional[int] = Field(
        default=None, description="能带来好心情吗，从 -10 到 10"
    )#心情值
    stamina: Optional[int] = Field(
        default=None, description="能补充多少能量，从 1 到 10"
    )#体力值
    meat: Optional[int] = Field(
        default=None, description="消耗肉类，从 1 到 3"
    )#消耗的肉类
    veg: Optional[int] = Field(
        default=None, description="消耗素类，从 1 到 3"
    )#消耗的素类
    food_description:str = Field(description="思考过程")#名称

class TownAgent:
    "智能体"
    agent_id: str
    agent_type: Literal["diligent", "lazy"]
    # 核心数值（0-100）
    __health: Literal["good","normal","bad"] #健康状态
    hunger: int #饥饿值
    mood: int #心情
    stamina: int #体力值
    action:list[TownAction] #行动列表
    llm:any #大模型
    def __init__(self,agent_id,agent_type:Literal["diligent", "lazy"]) -> None:
        self.agent_id=agent_id
        self.agent_type=agent_type
        self.__health=100
        self.hunger=0
        self.mood=100
        self.stamina=100
        self.action=[]
        pass
    def set_llm(self,llm):
        self.llm = llm
    def call_health(self):
        "健康设定"
        point =self.mood-self.hunger
        print(f"心情:{self.mood}-饥饿:{self.hunger}-体力{self.stamina}")
        if point>0 and point<=50:
            self.__health="normal"
        if point>50:
            self.__health ="good"
        if point<0:
            self.__health="bad"
        return self.__health
    def check_agent_health(self)->int:
        if self.call_health() == Literal["bad"]:
            return 0
        else :
            return 1
    def check_agent_action(self,stamina_cost:int,hunger_cost:int,hour:int)->int:
        if self.stamina<stamina_cost*hour or self.hunger<hunger_cost*hour or self.action.count>0:
            return 0
        else :
            return 1

    def agent_decide(self,world):
        action = MakeFood()
        if action.push_action(self,world,1) > 0:
            pass
        else:
            pass
        pass
    def decide_food(self,world:TownWorld)->TownFood:
        #决定食物制作
        query ="制作一份食物"
        prompt =make_food_prompt(world.meat,world.vegetables) +struct_output_prompt(TownFood)
        chain =  prompt| self.llm | pydantic_output(TownFood)
        resp =chain.invoke({"query": query})
        print(resp)
        return resp

class TownWorld:
    "世界"
    __datetime:int #日期
    __time:int #时间 0 到 24
    vegetables: int    # 素食食材（吨）
    meat: int          # 肉类食材（吨）
    __day_type:Literal["day","night"]
    food:dict[TownFood,int]    #食物数量
    agents:dict[str,TownAgent] #智能体
    def __init__(self) -> None:
        self.__datetime=0
        self.__time=0
        self.vegetables=0
        self.meat=0
        self.food=0
        self.agents={}
        self.food={}
        pass

    def call_day_type(self):
        "昼夜设定"
        if self.__time >=6 and self.__time <= 18:
            self.__day_type="day"
        else:
            self.__day_type="night"
        return self.__day_type
    
    def update_time(self,deltaTime:int):
        self.__time+=deltaTime
        if self.__time==24:
            self.__time=0
            self.__datetime+=1
        print(f"当前时间:{self.__datetime}天{self.__time}时")

class ImpactEffect:
    "影响行为"
    def impact(self,agent:TownAgent,value:int) -> None:
        agent.call_health()


class ImpactMood(ImpactEffect):
    "心情"
    def impact(self, agent: TownAgent, value: int) -> None:
        agent.mood+=value
        super().impact()


class ImpactHunger(ImpactEffect):
    "饥饿"
    def impact(self, agent: TownAgent, value: int) -> None:
        agent.hunger+=value
        super().impact()

class ImpactStam(ImpactEffect):
    "体力"
    def impact(self, agent: TownAgent, value: int) -> None:
        agent.stamina-=value
        super().impact()

class TownAction:
    _stamina_cost:int =0#体力消耗每小时
    _hunger_cost:int=0#饥饿消耗每小时
    _hour_cost:int = 0#目标行动时间
    __progress:int =0 #行动实时进度
    def push_action(self,agent:TownAgent,world:TownWorld,hour: int) -> int:
        "行动添加"
        self._hour_cost = hour
        #体力不够，饥饿值不够，有行动占用，健康值不足
        if agent.check_agent_action(self._stamina_cost,self._hunger_cost,hour) or agent.check_agent_health()<0:
            return 0
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
    food:TownFood
    def __init__(self) -> None:
        super().__init__()
    def push_action(self, agent: TownAgent, world: TownWorld, hour: int) -> int:
        #食物不够
        if world.meat+world.vegetables<3:
            print("食物不够")
            return 0
        if super().push_action(agent, world, hour) > 0:
            #决定食物制作
            self.food = agent.decide_food(world)
            return 1
        return 0
        
    def do_action(self, agent: TownAgent, world: TownWorld, hour: int):
      
        world.food[self.food]+=1
        ImpactHunger().impact(agent,self._hunger_cost*hour)
        ImpactStam().impact(agent,self._stamina_cost*hour)
       
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
            return 0
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