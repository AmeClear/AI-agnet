from langchain_core.prompts import ChatPromptTemplate
def make_food_prompt(meat_num:int,veg_num:int)->ChatPromptTemplate:
    return ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You Can Only use {meat_num} num meat and {veg_num} num vegetables",
        ),
    ]
    ).partial(meat_num = meat_num,veg_num = veg_num)