from pydantic import BaseModel
from dto.enums.tarot_cards import TarotCard


class ChatCommonRequest(BaseModel):
    chat: str


class ChatWithTarotCardCommonRequest(ChatCommonRequest):
    tarot_card: TarotCard
