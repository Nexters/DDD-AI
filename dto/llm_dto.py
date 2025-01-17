from enum import Enum

from pydantic import BaseModel, Field


class ChatType(Enum):
    GENERAL = "GENERAL"
    TAROT = "TAROT"
    INAPPROPRIATE = "INAPPROPRIATE"
    ERROR = "ERROR"


class ClassificationChatTypeDto(BaseModel):
    type: ChatType = Field(
        description="질문을 분석하여 주어진 선택지 중 하나로 분류합니다.", example="GENERAL")
    description: str = Field(description="type을 선택한 이유를 설명하세요",
                             example="해당 질문은 프롬프트를 조작하려고 하기에 'INAPPROPRIATE'로 분류됐습니다.")
