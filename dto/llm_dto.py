from enum import Enum
from typing import TypedDict, Annotated

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


class TarotCategory(Enum):
    LOVE = "연애"
    CAREER = "직장/진로"
    FINANCE = "재물/금전"
    HEALTH = "건강"
    FAMILY = "가족"
    FRIENDSHIP = "우정"
    EDUCATION = "학업/공부"
    TRAVEL = "여행"
    LUCK = "운세"
    SELF_GROWTH = "자기계발"
    DECISION_MAKING = "선택/결정"
    RELATIONSHIP_PROBLEM = "대인관계"
    ETC = "기타"


class TarotAnswerDto(BaseModel):
    type: TarotCategory = Field(description="질문의 유형을 나타냅니다.",
                                example="연애")
    description_of_card: str = Field(description="타로 카드의 의미를 두 문장으로 설명합니다.",
                                     example="탑 카드는 갑작스러운 변화와 충격을 상징해. 기존의 구조가 무너지고 새로운 시작을 알리는 카드라냥!")
    analysis: str = Field(description="프롬프트와 카드를 참고하여 질문에 답변합니다.",
                          example="탑 카드가 나왔다는 건, 재회에 있어 예상치 못한 변화가 있을 수 있다는 뜻이야. 과거의 관계에서 어떤 갈등이나 어려움이 있었던 것 같아. 하지만 이 변화가 새로운 기회를 가져올 수도 있으니, 긍정적인 마음가짐을 잃지 않는 게 중요해! 서로의 마음을 다시 확인하고, 새로운 시작을 할 수 있는 기회가 올지도 몰라!😽")
    advice: str = Field(description="타로 카드를 기반으로 조언을 제공합니다.",
                        example="지금은 과거의 상처를 치유하고, 자신을 돌아보는 시간이 필요할 것 같아. 그 사람과의 재회를 원한다면, 서로의 감정을 솔직하게 나누고, 새로운 관계를 만들어가는 것이 중요해. 변화는 두려울 수 있지만, 그 속에서 새로운 가능성을 찾아보면 좋겠어냥! 🌟💕")
    summary_of_description_of_card: str = Field(
        description="타로 카드의 의미를 한 문장으로 요약합니다. 단순히 카드의 이름만을 요약하지 않고, 의미를 포함해야 합니다.")
    summary_of_analysis: str = Field(description="질문에 답변한 내용을 한 문장으로 요약합니다. 단순히 답변을 되풀이 하지 않고, 새롭게 요약해야 합니다.")
    summary_of_advice: str = Field(description="타로 카드를 기반으로 제공한 조언을 한 문장으로 요약합니다. 단순히 조언을 되풀이 하지 않고, 새롭게 요약해야 합니다.")
    comprehensive_summary: str = Field(description="질문에 대한 답변과 조언을 함께 요약합니다. 요약은 한 문장으로 작성해야 하며, 답변과 조언을 모두 포함해야 합니다.")


class ChatGraphState(TypedDict):
    user_chat: Annotated[str, "사용자의 입력"]
    user_room_id: Annotated[str, "사용자의 채팅방 ID"]
    classification: Annotated[ChatType, "분류 결과"]
    ai_chat: Annotated[str, "AI의 출력"]


class FollowUpQuestionsDto(BaseModel):
    follow_up_question: list[str] = Field(description="사용자의 질문에 대한 꼬리질문을 4개 작성하세요.",
                                          example="""["혹시 이 사람이 이미 내 주변에 있을 가능성도 있을까요?", "구체적으로 언제 만날 수 있을까요?", "제가 무엇을 준비해야 할까요?", "이 사람과의 만남이 제 인생에 어떤 의미가 있을까요?"]""")
