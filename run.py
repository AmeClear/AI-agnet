from langchain_core.messages import HumanMessage, SystemMessage
from model import model
from pareser import parser
from prompt import prompt_template
from memory import with_message_history
# messages = {"language": "english", "text": "你好"}
# chain = prompt_template|model |parser
# resp = chain.invoke(messages)
config = {"configurable": {"session_id": "1"}}
resp = with_message_history.invoke(
    {"messages": [HumanMessage(content="hi! I'm todd")], "language": "Chinese"},
    config=config,
)
print(type(resp))
print(resp.content)
resp = with_message_history.invoke(
    {"messages": [HumanMessage(content="What's My Name")], "language": "Chinese"},
    config=config,
)
print(type(resp))
print(resp.content)