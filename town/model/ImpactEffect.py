from TownAgent import TownAgent


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