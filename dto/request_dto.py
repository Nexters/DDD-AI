from pydantic import BaseModel


class ChatCommonRequest(BaseModel):
    chat: str


class ChatWithTarotCardCommonRequest(ChatCommonRequest):
    tarot_card: str #TODO convert to enum
