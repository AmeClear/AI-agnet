from model import TownWorld
from model.TownWorld import TownFood


def make_food(world:TownWorld)-> TownFood:
    #定义值,输出给AI
    package ={"meat":0,"veg":0,"food_name":"","mood":0,"stam":0,"hunger":0}
    #AI思考
    world.meat-=package["meat"]
    world.vegetables-=package["veg"]
    return TownFood(package["food_name"],package["hunger"],package["mood"],package["stam"])