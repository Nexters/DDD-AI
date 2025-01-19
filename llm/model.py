import logging

from langchain.globals import set_llm_cache
from langchain_community.cache import InMemoryCache
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI

from dto.llm_dto import ClassificationChatTypeDto, ChatType, AnswerCommonDto
from prompt.prompt import get_basic_prompt_template, classify_chat_type_prompt, reply_general_question_prompt

set_llm_cache(InMemoryCache())

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    max_retries=2,
)


def llm_classify_chat(question: str):
    parser = PydanticOutputParser(pydantic_object=ClassificationChatTypeDto)
    chain = get_basic_prompt_template(classify_chat_type_prompt()) | llm | parser

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


def llm_reply_general_chat(question: str):
    parser = PydanticOutputParser(pydantic_object=AnswerCommonDto)
    chain = get_basic_prompt_template(reply_general_question_prompt()) | llm | parser

    try:
        return chain.invoke({
            "question": question,
            "format": parser.get_format_instructions()
        })
    except Exception as e:
        logging.error(f"An error occurred. error: {e}")
        return {
            "answer": "헉!! 답변하는 과정에서 오류가 발생했다냥😿 미안하다냥...🙀",
        }


def llm_reply_tarot_chat(
        question: str,
        tarot_card: str #TODO convert to enum
):
    parser = PydanticOutputParser(pydantic_object=AnswerCommonDto)
    chain = get_basic_prompt_template(reply_general_question_prompt()) | llm | parser

    try:
        return chain.invoke({
            "question": f"""
                뽑은 카드: {tarot_card}
                질문: {question}
            """,
            "format": parser.get_format_instructions()
        })
    except Exception as e:
        logging.error(f"An error occurred. error: {e}")
        return {
            "answer": "헉!! 답변하는 과정에서 오류가 발생했다냥😿 미안하다냥...🙀",
        }
