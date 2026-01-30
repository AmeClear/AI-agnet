

from typing import Literal

from TownAgent import TownAgent
class TownFood:
    name:str #名称
    hunger: int #饥饿值
    mood: int #心情
    stamina: int #体力值
    def __init__(self,name,hunger,mood,stamina) -> None:
        self.name = name
        self.hunger = hunger
        self.mood = mood
        self.stamina = stamina

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
        pass

    def call_day_type(self):
        "昼夜设定"
        if self.__time >=6 and self.__time <= 18:
            self.__day_type=Literal["day"]
        else:
            self.__day_type=Literal["night"]
        return self.__day_type
    
    def update_time(self,deltaTime:int):
        self.__time+=deltaTime
        print("当前时间:");print(self.__datetime+"天");print(self.__time+"时")
        if self.__time==24:
            self.__time=0
            self.__datetime+=1
    

