
from langchain_openai import ChatOpenAI

from env import DEEPSEEK_API,DEEPSEEK_BASE_URL

deepseek = ChatOpenAI(
    model="deepseek-v3.2",
    temperature=0.5,
    api_key=DEEPSEEK_API,
    base_url=DEEPSEEK_BASE_URL,
)
