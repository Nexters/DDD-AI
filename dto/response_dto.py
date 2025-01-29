from pydantic import BaseModel


class InternalErrorResponse(BaseModel):
    answer: str

    def __init__(self, answer: str = "헉!! 답변하는 과정에서 오류가 발생했다냥😿 미안하다냥...🙀"):
        super().__init__(answer=answer)


class ChatGraphResponse(BaseModel):
    classification: str
    answer: str

    def __init__(self, classification: str, answer: str):
        super().__init__(classification=classification, answer=answer)
