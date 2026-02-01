from model import TownWorld
from model.TownWorld import TownFood


def make_food(world:TownWorld)-> TownFood:
    meat =0
    veg =0
    food_name="a"
    mood =0
    stam =0
    hunger=0
    world.meat-=meat
    world.vegetables-=veg
    return TownFood(food_name,hunger,mood,stam)