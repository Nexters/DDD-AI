import logging

from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI

from dto.enums.tarot_cards import TarotCard
from dto.llm_dto import ClassificationChatTypeDto, ChatType, AnswerCommonDto, TarotAnswerDto, FollowUpQuestionsDto, SummarizeQuestionDto
from llm.chat_history import get_history_chain, remove_latest_message_history, get_latest_question, get_latest_ai_chat
from notification.discord_notification import notify_llm_error
from prompt.prompt import get_history_prompt_template, classify_chat_type_prompt, reply_general_question_prompt, \
    reply_inappropriate_question_prompt, reply_tarot_question_prompt, reply_question_question_prompt, \
    follow_up_question_prompt, get_basic_prompt_template, summarize_question_prompt

llm_4o = ChatOpenAI(
    model="gpt-4o",
    temperature=0.2,
    max_retries=0,
)

llm_4o_mini = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2,
    max_retries=2,
).with_fallbacks([llm_4o])


def llm_classify_chat(question: str, chat_room_id: str):
    parser = PydanticOutputParser(pydantic_object=ClassificationChatTypeDto)
    chain = get_history_prompt_template(classify_chat_type_prompt()) | llm_4o_mini
    history_chain = get_history_chain(chain) | parser

    try:
        result = history_chain.invoke({
            "question": question,
            "format": parser.get_format_instructions()
        }, config={"configurable": {"session_id": chat_room_id}})
        remove_latest_message_history(session_id=chat_room_id)
        return result
    except Exception as e:
        remove_latest_message_history(session_id=chat_room_id)
        logging.error(f"An error occurred in llm_classify_chat. error: {e}")
        notify_llm_error("llm_classify_chat", question, chat_room_id, e)
        return ClassificationChatTypeDto(type=ChatType.ERROR, description=f"An error occurred. error: {e}")


def llm_reply_general_chat(question: str, chat_room_id: str):
    parser = PydanticOutputParser(pydantic_object=AnswerCommonDto)
    chain = get_history_prompt_template(reply_general_question_prompt()) | llm_4o_mini
    history_chain = get_history_chain(chain) | parser

    try:
        return history_chain.invoke({
            "question": question,
            "format": parser.get_format_instructions()
        }, config={"configurable": {"session_id": chat_room_id}})
    except Exception as e:
        remove_latest_message_history(session_id=chat_room_id)
        logging.error(f"An error occurred in llm_reply_general_chat. error: {e}")
        notify_llm_error("llm_reply_general_chat", question, chat_room_id, e)


def llm_reply_question_chat(question: str, chat_room_id: str):
    parser = PydanticOutputParser(pydantic_object=AnswerCommonDto)
    chain = get_history_prompt_template(reply_question_question_prompt()) | llm_4o_mini
    history_chain = get_history_chain(chain) | parser

    try:
        return history_chain.invoke({
            "question": question,
            "format": parser.get_format_instructions()
        }, config={"configurable": {"session_id": chat_room_id}})
    except Exception as e:
        remove_latest_message_history(session_id=chat_room_id)
        logging.error(f"An error occurred in llm_reply_question_chat. error: {e}")
        notify_llm_error("llm_reply_question_chat", question, chat_room_id, e)


def llm_reply_tarot_chat(
        chat_room_id: str,
        tarot_card: TarotCard
):
    parser = PydanticOutputParser(pydantic_object=TarotAnswerDto)
    latest_question = get_latest_question(session_id=chat_room_id)
    chain = get_history_prompt_template(reply_tarot_question_prompt()) | llm_4o_mini
    history_chain = get_history_chain(chain) | parser
    try:
        return history_chain.invoke({
            "question": f"""
                뽑은 카드: {tarot_card.get_value()}
                질문: {latest_question.content}
            """,
            "format": parser.get_format_instructions()
        }, config={"configurable": {"session_id": chat_room_id}})
    except Exception as e:
        remove_latest_message_history(session_id=chat_room_id)
        logging.error(f"An error occurred in llm_reply_tarot_chat. error: {e}")
        notify_llm_error("llm_reply_tarot_chat", latest_question.content, chat_room_id, e)


def llm_reply_inappropriate_chat(question: str, chat_room_id: str):
    parser = PydanticOutputParser(pydantic_object=AnswerCommonDto)
    chain = get_history_prompt_template(reply_inappropriate_question_prompt()) | llm_4o_mini
    history_chain = get_history_chain(chain) | parser

    try:
        return history_chain.invoke({
            "question": question,
            "format": parser.get_format_instructions()
        }, config={"configurable": {"session_id": chat_room_id}})
    except Exception as e:
        remove_latest_message_history(session_id=chat_room_id)
        logging.error(f"An error occurred in llm_reply_inappropriate_chat. error: {e}")
        notify_llm_error("llm_reply_inappropriate_chat", question, chat_room_id, e)


def llm_suggest_follow_up_question(chat_room_id):
    follow_up_questions_parser = PydanticOutputParser(pydantic_object=FollowUpQuestionsDto)
    tarot_answer_parser = PydanticOutputParser(pydantic_object=TarotAnswerDto)
    chain = get_basic_prompt_template(follow_up_question_prompt()) | llm_4o_mini | follow_up_questions_parser
    latest_question = get_latest_question(session_id=chat_room_id)
    latest_ai_chat = get_latest_ai_chat(session_id=chat_room_id)

    latest_tarot_answer_dto = tarot_answer_parser.parse(latest_ai_chat.content)
    question = f"""
            사용자의 최근 질문과 선택한 카드 : {latest_question.content}
            사용자가 선택한 카드의 정보 : {latest_tarot_answer_dto.description_of_card}
            타로 전문가의 답볍 : {latest_tarot_answer_dto.analysis}
            타로 전문가의 조언 : {latest_tarot_answer_dto.advice}
            """
    try:
        return chain.invoke({
            "question": question,
            "format": follow_up_questions_parser.get_format_instructions()
        })
    except Exception as e:
        logging.error(f"An error occurred in llm_suggest_follow_up_question. error: {e}")
        notify_llm_error("llm_suggest_follow_up_question", question, chat_room_id, e)


def llm_summarize_question(question: str):
    summarize_questions_parser = PydanticOutputParser(pydantic_object=SummarizeQuestionDto)
    chain = get_basic_prompt_template(summarize_question_prompt()) | llm_4o_mini | summarize_questions_parser

    try:
        return chain.invoke({
            "question": f"사용자의 질문: {question}",
            "format": summarize_questions_parser.get_format_instructions()
        })
    except Exception as e:
        logging.error(f"An error occurred in llm_summarize_question. error: {e}")
        notify_llm_error("llm_summarize_question", question, "None", e)
