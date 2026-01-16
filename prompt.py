#提示词
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
system_template = (
            "system",
             "You are a helpful assistant. Answer all questions to the best of your ability in {language}.",
        )
prompt_template = ChatPromptTemplate.from_messages(
    [system_template, MessagesPlaceholder(variable_name="messages"),]
)