from pydantic import BaseModel


class ChatCommonRequest(BaseModel):
    chat: str
