from typing import Literal
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
