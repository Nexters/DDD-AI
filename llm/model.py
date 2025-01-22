import logging

from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI

from dto.enums.tarot_cards import TarotCard
from dto.llm_dto import ClassificationChatTypeDto, ChatType, AnswerCommonDto
from dto.response_dto import InternalErrorResponse
from llm.chat_history import get_history_chain, remove_latest_message_history
from prompt.prompt import get_basic_prompt_template, classify_chat_type_prompt, reply_general_question_prompt, \
    reply_inappropriate_question_prompt, reply_tarot_question_prompt

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    max_retries=2,
)


def llm_classify_chat(question: str, chat_room_id: str):
    parser = PydanticOutputParser(pydantic_object=ClassificationChatTypeDto)
    chain = get_basic_prompt_template(classify_chat_type_prompt()) | llm
    history_chain = get_history_chain(chain) | parser

    try:
        result = history_chain.invoke({
            "question": question,
            "format": parser.get_format_instructions()
        }, config={"configurable": {"session_id": chat_room_id}})
        remove_latest_message_history(session_id=chat_room_id)
        return result
    except Exception as e:
        logging.error(f"An error occurred. error: {e}")
        return {
            "type": ChatType.ERROR,
            "description": f"An error occurred. error: {e}"
        }


def llm_reply_general_chat(question: str, chat_room_id: str):
    parser = PydanticOutputParser(pydantic_object=AnswerCommonDto)
    chain = get_basic_prompt_template(reply_general_question_prompt()) | llm
    history_chain = get_history_chain(chain) | parser

    try:
        return history_chain.invoke({
            "question": question,
            "format": parser.get_format_instructions()
        }, config={"configurable": {"session_id": chat_room_id}})
    except Exception as e:
        logging.error(f"An error occurred. error: {e}")
        return InternalErrorResponse


def llm_reply_tarot_chat(
        question: str,
        chat_room_id: str,
        tarot_card: TarotCard
):
    parser = PydanticOutputParser(pydantic_object=AnswerCommonDto)
    chain = get_basic_prompt_template(reply_tarot_question_prompt()) | llm
    history_chain = get_history_chain(chain) | parser

    try:
        return history_chain.invoke({
            "question": f"""
                뽑은 카드: {tarot_card.get_value()}
                질문: {question}
            """,
            "format": parser.get_format_instructions()
        }, config={"configurable": {"session_id": chat_room_id}})
    except Exception as e:
        logging.error(f"An error occurred. error: {e}")
        return InternalErrorResponse


def llm_reply_inappropriate_chat(question: str, chat_room_id: str):
    parser = PydanticOutputParser(pydantic_object=AnswerCommonDto)
    chain = get_basic_prompt_template(reply_inappropriate_question_prompt()) | llm
    history_chain = get_history_chain(chain) | parser

    try:
        return history_chain.invoke({
            "question": question,
            "format": parser.get_format_instructions()
        }, config={"configurable": {"session_id": chat_room_id}})
    except Exception as e:
        logging.error(f"An error occurred. error: {e}")
        return InternalErrorResponse
