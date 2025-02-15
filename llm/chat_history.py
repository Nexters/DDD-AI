from datetime import datetime, timedelta

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory


class ChatHistory:
    history: ChatMessageHistory
    updated_date: datetime
    _MAX_HISTORY_LENGTH = 6
    _REMOVE_LATEST_MESSAGES_SIZE = 2

    def __init__(self):
        self.history = ChatMessageHistory()
        self.updated_date = datetime.now()

    def get_history(self) -> ChatMessageHistory:
        self.updated_date = datetime.now()
        self.trim_history()
        return self.history

    def trim_history(self):
        if len(self.history.messages) > self._MAX_HISTORY_LENGTH:
            self.history.messages = self.history.messages[-self._MAX_HISTORY_LENGTH:]

    def remove_latest_message(self):
        if self.history.messages:
            self.history.messages = self.history.messages[:-self._REMOVE_LATEST_MESSAGES_SIZE] if (
                    len(self.history.messages) >= self._REMOVE_LATEST_MESSAGES_SIZE) else []

    def get_latest_question(self):
        if self.history.messages and len(self.history.messages) > 1:
            return self.history.messages[-2]
        return None

    def get_latest_ai_chat(self):
        if self.history.messages and len(self.history.messages) > 1:
            return self.history.messages[-1]
        return None

    def is_outdated_hours(self, hours) -> bool:
        return datetime.now() - self.updated_date > timedelta(hours=hours)


store: dict[str, ChatHistory] = {
}


def get_all_session_histories():
    return store.items()


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatHistory()
    return store[session_id].get_history()


def remove_session_history(session_id: str):
    if session_id in store:
        store.pop(session_id)
    return


def remove_latest_message_history(session_id: str):
    if session_id not in store:
        return
    store[session_id].remove_latest_message()


def get_latest_question(session_id: str):
    if session_id not in store:
        return None
    return store[session_id].get_latest_question()


def get_latest_ai_chat(session_id: str):
    if session_id not in store:
        return None
    return store[session_id].get_latest_ai_chat()


def get_history_chain(chain):
    return RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="question",
        history_messages_key="chat_history",
    )
