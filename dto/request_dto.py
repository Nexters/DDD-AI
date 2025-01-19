from pydantic import BaseModel


class ChatCommonRequest(BaseModel):
    chat: str


class ChatWithTarotCardCommonRequest(ChatCommonRequest):
    chat: str
    tarot_card: str #TODO convert to enum
