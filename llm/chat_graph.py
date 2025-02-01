from langgraph.constants import START, END
from langgraph.graph import StateGraph

from dto.llm_dto import ChatGraphState, ChatType
from llm.model import llm_classify_chat, llm_reply_general_chat, llm_reply_question_chat, llm_reply_inappropriate_chat


def classify_chat(state: ChatGraphState):
    user_chat = state["user_chat"]
    user_room_id = state["user_room_id"]

    classification_result = llm_classify_chat(user_chat, user_room_id)
    return {
        "classification": classification_result.type,
    }


def route_classified_chat(state: ChatGraphState):
    classification = state["classification"]

    if classification == ChatType.GENERAL:
        return "reply_general_chat"
    elif classification == ChatType.TAROT:
        return "reply_question_chat"
    elif classification == ChatType.INAPPROPRIATE:
        return "reply_inappropriate_chat"
    else:
        return "ERROR"


def reply_general_chat(state: ChatGraphState):
    user_chat = state["user_chat"]
    user_room_id = state["user_room_id"]

    reply_result = llm_reply_general_chat(user_chat, user_room_id)
    return {
        "ai_chat": reply_result.answer,
    }


def reply_question_chat(state: ChatGraphState):
    user_chat = state["user_chat"]
    user_room_id = state["user_room_id"]

    reply_result = llm_reply_question_chat(user_chat, user_room_id)
    return {
        "ai_chat": reply_result.answer,
    }


def reply_inappropriate_chat(state: ChatGraphState):
    user_chat = state["user_chat"]
    user_room_id = state["user_room_id"]

    reply_result = llm_reply_inappropriate_chat(user_chat, user_room_id)
    return {
        "ai_chat": reply_result.answer,
    }


def get_chat_graph():
    graph_builder = StateGraph(ChatGraphState)

    graph_builder.add_node("classify_chat", classify_chat)
    graph_builder.add_node("reply_general_chat", reply_general_chat)
    graph_builder.add_node("reply_question_chat", reply_question_chat)
    graph_builder.add_node("reply_inappropriate_chat", reply_inappropriate_chat)

    graph_builder.add_edge(START, "classify_chat")
    graph_builder.add_conditional_edges("classify_chat", route_classified_chat, {
        "reply_general_chat": "reply_general_chat",
        "reply_question_chat": "reply_question_chat",
        "reply_inappropriate_chat": "reply_inappropriate_chat",
        "ERROR": END,
    })
    graph_builder.add_edge("reply_general_chat", END)
    graph_builder.add_edge("reply_question_chat", END)
    graph_builder.add_edge("reply_inappropriate_chat", END)

    graph = graph_builder.compile()
    return graph
