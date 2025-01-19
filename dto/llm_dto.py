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


class AnswerCommonDto(BaseModel):
    answer: str = Field(description="프롬프트를 참고하여 질문에 답변합니다.",
                        example="좋은 아침이다냥~ 오늘도 햇살처럼 따뜻한 하루가 되길 바란다냥!! 혹시 오늘 어떤 계획이 있나냥!? 아니면 타로 카드로 오늘의 운세를 알아보는건 어떠냥? 궁금한 거 있으면 언제든지 말해달라냥! 🐾✨")
