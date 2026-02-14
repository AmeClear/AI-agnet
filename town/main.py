
from agent.AgentThinking import decide_food

from agent.llm import openAI
from agent.llm import deepseek

if __name__ == "__main__":
    decide_food(openAI)
    decide_food(deepseek)
