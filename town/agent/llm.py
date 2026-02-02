'''
Author: clear.fang 729848336@qq.com
Date: 2026-01-14 20:26:55
LastEditors: clear.fang 729848336@qq.com
LastEditTime: 2026-01-26 18:10:29
FilePath: \AI-agnet\llm.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''

#模型库
from langchain_openai import ChatOpenAI

from env import DEEPSEEK_API,DEEPSEEK_BASE_URL
import tiktoken
llm = ChatOpenAI(
    model="deepseek-v3.2",
    temperature=0.5,
    api_key=DEEPSEEK_API,
    base_url=DEEPSEEK_BASE_URL,
)
