from pydantic import BaseModel

from dto.enums.tarot_cards import TarotCard


class ChatCommonRequest(BaseModel):
    chat: str
    chat_room_id: str
    trace_id: str | None = None


class ChatWithTarotCardCommonRequest(BaseModel):
    tarot_card: TarotCard
    chat_room_id: str
