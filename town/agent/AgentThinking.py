'''
Author: clear.fang 729848336@qq.com
Date: 2026-02-02 14:01:46
LastEditors: clear.fang 729848336@qq.com
LastEditTime: 2026-02-10 16:54:24
FilePath: \AI-agnet\town\agent\AgentThinking.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from agent.OutPuts.PydanticPareser import pydantic_output
from agent.Prompts.StructOutputPrompt import struct_output_prompt
from model.ObjectDefine import TownFood

def decide_food(llm)->TownFood:
    #决定食物制作
    query ="制作一份食物"
    chain = struct_output_prompt(TownFood) | llm | pydantic_output(TownFood)
    resp =chain.invoke({"query": query})
    print(resp)
    return resp