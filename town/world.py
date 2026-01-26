import asyncio
from model import SimulationState
from agent_work_graph import decide_and_act
import json
from datetime import datetime
from logger import SimulationLogger
class TownSimulator:
    """小镇模拟器（修复版）"""
    
    def __init__(self):
        # 初始化世界状态
        self.state: SimulationState = {
            "world": {
                "current_hour": 0,
                "vegetables": 10,
                "meat": 10,
                "planted_crops": {},
                "raising_animals": {}
            },
            "diligent": {
                "agent_id": "diligent",
                "agent_type": "diligent",
                "health": 100,
                "hunger": 0,
                "mood": 100,
                "stamina": 100,
                "labour_bias": 0.7,
                "rest_bias": 0.3,
                "location": "home",
                "last_action": "init",
                "last_action_params": {}
            },
            "lazy": {
                "agent_id": "lazy",
                "agent_type": "lazy",
                "health": 100,
                "hunger": 0,
                "mood": 100,
                "stamina": 100,
                "labour_bias": 0.3,
                "rest_bias": 0.7,
                "location": "home",
                "last_action": "init",
                "last_action_params": {}
            },
            "logs": []
        }
        # 初始化日志记录器
        self.logger = SimulationLogger()
    def _update_world_resources(self):
        """更新世界资源：检查作物成熟、动物成熟"""
        world = self.state["world"]
        current = world["current_hour"]
        
        # 收获成熟的作物（24小时生长）
        to_harvest = []
        for crop_id, crop in list(world["planted_crops"].items()):
            if current - crop.get("plant_hour", 0) >= 24:
                to_harvest.append(crop_id)
                world["vegetables"] += 2  # 收获2吨
                print(f"  [世界] 作物 {crop_id} 成熟，收获2吨蔬菜")
        
        for crop_id in to_harvest:
            del world["planted_crops"][crop_id]
        
        # 屠宰成熟的动物（48小时生长）
        to_slaughter = []
        for animal_id, animal in list(world["raising_animals"].items()):
            if current - animal.get("raise_hour", 0) >= 48:
                to_slaughter.append(animal_id)
                world["meat"] += 1  # 获得1吨肉
                print(f"  [世界] 动物 {animal_id} 成熟，获得1吨肉")
        
        for animal_id in to_slaughter:
            del world["raising_animals"][animal_id]
    
    def _apply_action_effects(self, agent_id: str):
        """应用行动对世界的影响"""
        agent = self.state[agent_id]
        world = self.state["world"]
        
        if agent["last_action"] == "cook_and_eat":
            params = agent["last_action_params"]
            world["vegetables"] -= params["veg_used"]
            world["meat"] -= params["meat_used"]
        
        elif agent["last_action"] == "plant_crops":
            crop_id = f"crop_{world['current_hour']}_{agent_id}"
            world["planted_crops"][crop_id] = {
                "plant_hour": world["current_hour"],
                "planted_by": agent_id
            }
        
        elif agent["last_action"] == "raise_animals":
            animal_id = f"animal_{world['current_hour']}_{agent_id}"
            world["raising_animals"][animal_id] = {
                "raise_hour": world["current_hour"],
                "raised_by": agent_id
            }
    
    def _update_health(self, agent_id: str):
        """更新健康值"""
        agent = self.state[agent_id]
        
        # 计算各项惩罚
        hunger_penalty = max(0, agent["hunger"] - 50) / 50 * 100
        mood_penalty = max(0, 50 - agent["mood"])
        stamina_penalty = max(0, 20 - agent["stamina"]) / 20 * 100
        
        # 综合健康值
        agent["health"] = 100 - (hunger_penalty + mood_penalty + stamina_penalty) / 3
        agent["health"] = max(0, min(100, int(agent["health"])))
    
    async def simulate_one_hour(self):
        """模拟一个小时"""
        world = self.state["world"]
        hour = world["current_hour"]
        day = hour // 24 + 1
        hour_in_day = hour % 24
        
        print(f"\n=== 第{day}天 {hour_in_day:02d}:00 ===")
        
        # 更新世界资源
        self._update_world_resources()
        
        # 顺序模拟两个智能体（现在使用await调用异步函数）
        for agent_id in ["diligent", "lazy"]:
            # 执行决策和行动（使用await调用异步函数）
            new_agent_state = await decide_and_act(self.state, agent_id)
            self.state[agent_id].update(new_agent_state)
            
            # 应用行动对世界的影响
            self._apply_action_effects(agent_id)
            
            # 体力自然消耗（如果不是休息/睡觉）
            if self.state[agent_id]["last_action"] not in ["sleep", "rest_read", "rest_game", "rest_sing"]:
                self.state[agent_id]["stamina"] = max(0, self.state[agent_id]["stamina"] - 5)
            
            # 更新健康值
            self._update_health(agent_id)
            
            # 记录日志
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "day": day,
                "hour": hour,
                "agent": agent_id,
                "action": self.state[agent_id]["last_action"],
                "action_params": self.state[agent_id]["last_action_params"],
                "stats": {
                    "health": self.state[agent_id]["health"],
                    "hunger": self.state[agent_id]["hunger"],
                    "mood": self.state[agent_id]["mood"],
                    "stamina": self.state[agent_id]["stamina"]
                },
                "world_snapshot": {
                    "vegetables": world["vegetables"],
                    "meat": world["meat"],
                    "crops_count": len(world["planted_crops"]),
                    "animals_count": len(world["raising_animals"])
                }
            }
            self.state["logs"].append(log_entry)
            
            # 打印状态
            stats = log_entry["stats"]
            print(f"{agent_id:8s} | 行动: {self.state[agent_id]['last_action']:20s} | "
                  f"健康:{stats['health']:3d} 饥饿:{stats['hunger']:3d} "
                  f"心情:{stats['mood']:3d} 体力:{stats['stamina']:3d}")
        
        # 时间前进
        world["current_hour"] += 1
    
    async def run_7_days(self):
        """运行7天模拟"""
        print("="*60)
        print("开始7天A/B测试模拟：勤奋型 vs 懒散型")
        print("="*60)
        
        total_hours = 7 * 24
        
        try:
            for hour in range(total_hours):
                await self.simulate_one_hour()
                
                # 检查生存失败
                for agent_id in ["diligent", "lazy"]:
                    if self.state[agent_id]["health"] <= 0:
                        print(f"\n⚠️ {agent_id} 生存失败！模拟提前结束。")
                        await self._generate_report(early_stop=True)
                        return
            
            print("\n" + "="*60)
            print("7天模拟顺利完成！")
            self._generate_report()
            
        except Exception as e:
            print(f"\n❌ 模拟过程中出现错误: {e}")
            import traceback
            traceback.print_exc()
    
    def _generate_report(self, early_stop=False):
        """生成分析报告"""
        print("\n" + "="*60)
        print("模拟分析报告")
        print("="*60)
        
        logs = self.state["logs"]
        
        # 1. 关键指标对比
        print("\n【关键指标对比】")
        print(f"{'指标':<10} | {'勤奋型':<10} | {'懒散型':<10} | {'差异'}")
        print("-" * 45)
        
        metrics = ["health", "hunger", "mood", "stamina"]
        for metric in metrics:
            diligent_vals = [log["stats"][metric] for log in logs 
                           if log["agent"] == "diligent" and log["hour"] % 24 == 0]
            lazy_vals = [log["stats"][metric] for log in logs 
                        if log["agent"] == "lazy" and log["hour"] % 24 == 0]
            
            d_avg = sum(diligent_vals)/len(diligent_vals) if diligent_vals else 0
            l_avg = sum(lazy_vals)/len(lazy_vals) if lazy_vals else 0
            
            print(f"{metric:<10} | {d_avg:>8.1f}  | {l_avg:>8.1f}  | {d_avg-l_avg:>+6.1f}")
        
        # 2. 行为统计
        print("\n【行为分布】")
        all_actions = set(log["action"] for log in logs)
        
        for agent_id in ["diligent", "lazy"]:
            print(f"\n{agent_id} 的行为分布:")
            agent_logs = [log for log in logs if log["agent"] == agent_id]
            
            for action in sorted(all_actions):
                count = len([log for log in agent_logs if log["action"] == action])
                if count > 0:
                    print(f"  {action:20s}: {count:3d}次")
        
        # 3. 最终状态
        print("\n【最终状态】")
        world = self.state["world"]
        print(f"模拟时间: 第{world['current_hour']//24}天 {world['current_hour']%24:02d}:00")
        print(f"世界资源: 蔬菜{world['vegetables']}吨, 肉类{world['meat']}吨")
        print(f"进行中: {len(world['planted_crops'])}个作物, {len(world['raising_animals'])}只动物")
        
        for agent_id in ["diligent", "lazy"]:
            agent = self.state[agent_id]
            print(f"\n{agent_id}:")
            print(f"  健康:{agent['health']} 饥饿:{agent['hunger']} 心情:{agent['mood']} 体力:{agent['stamina']}")
        
        # 4. 保存日志
        filename = f"simulation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump({
                "final_state": self.state,
                "logs": logs,
                "early_stop": early_stop
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\n详细日志已保存至: {filename}")

# ==================== 5. 运行模拟 ====================
if __name__ == "__main__":
    print("正在启动小镇模拟器...")
    simulator = TownSimulator()
    asyncio.run(simulator.run_7_days())