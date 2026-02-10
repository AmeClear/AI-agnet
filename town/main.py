
from agent.AgentThinking import decide_food

from agent.LLM import openAI
from agent.LLM import deepseek

if __name__ == "__main__":
    decide_food(openAI)
    decide_food(deepseek)
