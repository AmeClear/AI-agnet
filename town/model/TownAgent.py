from typing import Literal

from .TownAction import TownAction


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

    def __init__(self,agent_id,agent_type:Literal["diligent", "lazy"]) -> None:
        self.agent_id=agent_id
        self.agent_type=agent_type
        self.__health=100
        self.hunger=0
        self.mood=100
        self.stamina=100
        self.action=[]
        pass
    def call_health(self):
        "健康设定"
        point =self.mood-self.hunger
        if point>0 and point<=50:
            self.__health="normal"
        if point>50:
            self.__health ="good"
        if point<0:
            self.__health="bad"
        return self.__health
    
    def decide(self):
        "智能体决策"
        pass
    
