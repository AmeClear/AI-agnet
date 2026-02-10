'''
Author: clear.fang 729848336@qq.com
Date: 2026-01-26 17:31:43
LastEditors: clear.fang 729848336@qq.com
LastEditTime: 2026-02-09 16:06:27
FilePath: \AI-agnet\town\model\TownWorld.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''


from __future__ import annotations  # 放在文件最顶部
from typing import Literal
from typing import TYPE_CHECKING
# 只在类型检查时导入
if TYPE_CHECKING:
    from .TownAgent import TownAgent
    from .ObjectDefine import TownFood

    

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
    

