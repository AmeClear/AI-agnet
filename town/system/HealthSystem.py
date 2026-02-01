from __future__ import annotations  # 放在文件最顶部
from typing import TYPE_CHECKING

from typing import Literal
# 只在类型检查时导入
if TYPE_CHECKING:
    from model.TownAgent import TownAgent

def check_agent_health(agent:TownAgent)->int:
    if agent.call_health() == Literal["bad"]:
        return -1
    else :
        return 1
def check_agent_action(agent:TownAgent,stamina_cost:int,hunger_cost:int,hour:int)->int:
    if agent.stamina<stamina_cost*hour or agent.hunger<hunger_cost*hour or agent.action.count>0:
        return -1
    else :
        return 1
