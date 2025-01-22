from contextlib import asynccontextmanager

from fastapi import FastAPI, Response

from dto.request_dto import ChatCommonRequest, ChatWithTarotCardCommonRequest
from llm.model import llm_classify_chat, llm_reply_general_chat, llm_reply_tarot_chat, llm_reply_inappropriate_chat
from scheduler.history_scheduler import scheduler


@asynccontextmanager
async def lifespan(_app):
    scheduler.start()
    yield


app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False}, lifespan=lifespan)


@app.get("/health_check")
def health_check():
    return Response(status_code=200)


@app.post("/api/v1/classify/chat")
def classify_chat(req: ChatCommonRequest):
    return llm_classify_chat(
        question=req.chat,
        chat_room_id=req.chat_room_id
    )


@app.post("/api/v1/reply/general-chat")
def reply_general_chat(req: ChatCommonRequest):
    return llm_reply_general_chat(
        question=req.chat,
        chat_room_id=req.chat_room_id
    )


@app.post("/api/v1/reply/tarot-chat")
def reply_tarot_chat(req: ChatWithTarotCardCommonRequest):
    return llm_reply_tarot_chat(
        # TODO 논의 필요
        # question=req.chat,
        chat_room_id=req.chat_room_id,
        tarot_card=req.tarot_card
    )


@app.post("/api/v1/reply/inappropriate-chat")
def reply_tarot_chat(req: ChatCommonRequest):
    return llm_reply_inappropriate_chat(
        question=req.chat,
        chat_room_id=req.chat_room_id
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
