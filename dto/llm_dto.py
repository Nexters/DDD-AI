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


class TarotAnswerDto(BaseModel):
    type: str = Field(description="질문의 유형을 나타냅니다.",
                        example="연애, 애정, 금전, 학업 등")
    description_of_card: str = Field(description="타로 카드의 의미를 설명합니다.",
                                     example="마법사 카드는 새로운 시작과 창조적인 에너지를 상징한다냥!")
    analysis: str = Field(description="프롬프트와 카드를 참고하여 질문에 답변합니다.",
                        example="함께라면 서로의 힘을 잘 활용해서 멋진 관계를 만들어갈 수 있을 거야. 마법사처럼 너희의 의사소통과 이해가 잘 이루어진다면, 오래오래 만날 수 있을 것 같아! 서로의 마음을 잘 표현하고, 함께하는 시간을 소중히 여기는 게 중요해. 그러니 긍정적인 에너지를 잃지 말고, 서로를 믿고 지지해주면 좋겠어냥! 💖✨")
    advice: str = Field(description="타로 카드를 기반으로 한 조언을 제공합니다.",
                        example="오늘은 서로의 의견을 존중하고, 서로를 이해하는 게 중요할 거 같다냥. 서로의 생각과 마음을 솔직하게 표현하면서, 서로를 더 잘 알아가는 시간을 가지면 좋을 거 같아냥. 또한 서로를 응원하고 지지해주는 마음을 잊지 말고, 서로에게 힘이 되어주는 관계를 만들어나가면 좋겠다냥! 🌟💕")
    summary_of_description_of_card: str = Field(description="타로 카드의 의미를 한 문장으로 요약합니다.",
                                           example="")
    summary_of_analysis: str = Field(description="분석을 한 문장으로 요약합니다.",
                                             example="")
    summary_of_advice: str = Field(description="조언을 한 문장으로 요약합니다.",
                                             example="")
