from langchain_core.messages import HumanMessage, SystemMessage
from model import deepseek
from pareser import parser
from prompt import prompt_template

messages = {"language": "english", "text": "你好"}
chain = prompt_template|deepseek |parser
resp = chain.invoke(messages)
print(type(resp))
print(resp)