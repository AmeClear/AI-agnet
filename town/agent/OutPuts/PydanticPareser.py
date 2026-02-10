'''

from town.model.ObjectDefine import TownFood
Author: clear.fang 729848336@qq.comTownFood
Date: 2026-02-10 16:07:17
LastEditors: clear.fang 729848336@qq.com
LastEditTime: 2026-02-10 16:36:38
FilePath: \AI-agnet\town\agent\tool\PydanticPareser.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from langchain_core.output_parsers import PydanticOutputParser



def pydantic_output(pydantic_object)->PydanticOutputParser:
    return PydanticOutputParser(pydantic_object=pydantic_object)