from pydantic import BaseModel

from dto.enums.tarot_cards import TarotCard


class ChatCommonRequest(BaseModel):
    chat: str
    chat_room_id: str


class ChatWithTarotCardCommonRequest(ChatCommonRequest):
    tarot_card: TarotCard
