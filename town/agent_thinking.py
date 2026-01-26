'''
Author: clear.fang 729848336@qq.com
Date: 2026-01-26 18:06:33
LastEditors: clear.fang 729848336@qq.com
LastEditTime: 2026-01-26 18:10:54
FilePath: \AI-agnet\town\cook_eat.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
# 新增函数：调用LLM评定这顿饭
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from llm import llm
import json


async def ai_evaluate_meal(ingredients: dict, agent_mood: int) -> dict:
    """AI评定饭菜质量和心情影响"""
    prompt = ChatPromptTemplate.from_messages([
        ("system", """你是一个生活模拟器的评定系统。请根据以下信息，为这顿饭评定数值：
         - 食材比例：{veg}吨蔬菜，{meat}吨肉类
         - 做饭者当前心情：{mood}/100
         请输出一个JSON对象，包含：
         - `satiation` (饱腹感提升): 10到30的整数
         - `deliciousness` (美食度提升): 10到30的整数
         - `description` (简短描述): 对这顿饭的一句话描述"""),
        ("human", "请评定这顿饭。")
    ])
    
    chain = prompt | llm
    response = await chain.ainvoke({
        "veg": ingredients["veg"],
        "meat": ingredients["meat"],
        "mood": agent_mood
    })
    
    # 解析JSON响应
    try:
        return json.loads(response.content)
    except:
        # 备选方案：如果AI返回非JSON，使用默认值
        return {"satiation": 20, "deliciousness": 20, "description": "一顿普通的饭"}