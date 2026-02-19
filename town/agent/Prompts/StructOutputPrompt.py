from langchain_core.prompts import ChatPromptTemplate
from agent.OutPuts.PydanticPareser import pydantic_output
def struct_output_prompt(classType)->ChatPromptTemplate:
    return ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Answer the user query. Wrap the output in `json` tags\n{format_instructions}",
        ),
        ("human", "{query}"),
    ]
    ).partial(format_instructions=pydantic_output(classType).get_format_instructions())