from datetime import datetime, timedelta

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory


class ChatHistory:
    history: ChatMessageHistory
    updated_date: datetime

    def __init__(self):
        self.history = ChatMessageHistory()
        self.updated_date = datetime.now()

    def get_history(self) -> ChatMessageHistory:
        self.updated_date = datetime.now()
        self.trim_history()
        return self.history

    def trim_history(self):
        self.history.messages = self.history.messages[-3:]

    def is_outdated_hours(self, hours) -> bool:
        return datetime.now() - self.updated_date > timedelta(hours=hours)


store = {
}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatHistory()
    return store[session_id].get_history()


def remove_session_history(session_id: str):
    if session_id in store:
        store.pop(session_id)
    return


def get_history_chain(chain):
    return RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="question",
        history_messages_key="chat_history",
    )
