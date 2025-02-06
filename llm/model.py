import logging

from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI

from dto.enums.tarot_cards import TarotCard
from dto.llm_dto import ClassificationChatTypeDto, ChatType, AnswerCommonDto, TarotAnswerDto
from dto.response_dto import InternalErrorResponse
from llm.chat_history import get_history_chain, remove_latest_message_history, get_latest_question
from prompt.prompt import get_basic_prompt_template, classify_chat_type_prompt, reply_general_question_prompt, \
    reply_inappropriate_question_prompt, reply_tarot_question_prompt, reply_question_question_prompt

llm_4o = ChatOpenAI(
    model="gpt-4o",
    temperature=0.2,
    max_retries=0,
)

llm_4o_mini = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2,
    max_retries=1,
).with_fallbacks([llm_4o])


def llm_classify_chat(question: str, chat_room_id: str):
    parser = PydanticOutputParser(pydantic_object=ClassificationChatTypeDto)
    chain = get_basic_prompt_template(classify_chat_type_prompt()) | llm_4o_mini
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
        return ClassificationChatTypeDto(type=ChatType.ERROR, description=f"An error occurred. error: {e}")


def llm_reply_general_chat(question: str, chat_room_id: str):
    parser = PydanticOutputParser(pydantic_object=AnswerCommonDto)
    chain = get_basic_prompt_template(reply_general_question_prompt()) | llm_4o_mini
    history_chain = get_history_chain(chain) | parser

    try:
        return history_chain.invoke({
            "question": question,
            "format": parser.get_format_instructions()
        }, config={"configurable": {"session_id": chat_room_id}})
    except Exception as e:
        logging.error(f"An error occurred. error: {e}")
        return InternalErrorResponse()


def llm_reply_question_chat(question: str, chat_room_id: str):
    parser = PydanticOutputParser(pydantic_object=AnswerCommonDto)
    chain = get_basic_prompt_template(reply_question_question_prompt()) | llm_4o
    history_chain = get_history_chain(chain) | parser

    try:
        return history_chain.invoke({
            "question": question,
            "format": parser.get_format_instructions()
        }, config={"configurable": {"session_id": chat_room_id}})
    except Exception as e:
        logging.error(f"An error occurred. error: {e}")
        return InternalErrorResponse()


def llm_reply_tarot_chat(
        chat_room_id: str,
        tarot_card: TarotCard
):
    parser = PydanticOutputParser(pydantic_object=TarotAnswerDto)
    chain = get_basic_prompt_template(reply_tarot_question_prompt()) | llm_4o_mini
    history_chain = get_history_chain(chain) | parser
    latest_question = get_latest_question(session_id=chat_room_id)

    try:
        return history_chain.invoke({
            "question": f"""
                뽑은 카드: {tarot_card.get_value()}
                질문: {latest_question.content}
            """,
            "format": parser.get_format_instructions()
        }, config={"configurable": {"session_id": chat_room_id}})
    except Exception as e:
        logging.error(f"An error occurred. error: {e}")
        return InternalErrorResponse()


def llm_reply_inappropriate_chat(question: str, chat_room_id: str):
    parser = PydanticOutputParser(pydantic_object=AnswerCommonDto)
    chain = get_basic_prompt_template(reply_inappropriate_question_prompt()) | llm_4o_mini
    history_chain = get_history_chain(chain) | parser

    try:
        return history_chain.invoke({
            "question": question,
            "format": parser.get_format_instructions()
        }, config={"configurable": {"session_id": chat_room_id}})
    except Exception as e:
        logging.error(f"An error occurred. error: {e}")
        return InternalErrorResponse()
