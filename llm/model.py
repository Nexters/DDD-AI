from langchain.globals import set_llm_cache
from langchain_community.cache import InMemoryCache
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI

from dto.llm_dto import ClassificationChatTypeDto, ChatType
from prompt.prompt import get_classify_chat_type_prompt_template

set_llm_cache(InMemoryCache())

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    max_retries=2,
)


def llm_classify_chat(question: str):
    parser = PydanticOutputParser(pydantic_object=ClassificationChatTypeDto)
    chain = get_classify_chat_type_prompt_template() | llm | parser

    try:
        return chain.invoke({
            "question": question,
            "format": parser.get_format_instructions()
        })
    except Exception as e:
        return {
            "type": ChatType.ERROR,
            "description": f"An error occurred. error: {e}"
        }
