from pydantic import BaseModel, Field
from typing import Optional

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