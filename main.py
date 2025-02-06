from contextlib import asynccontextmanager

from fastapi import FastAPI, Response
from starlette.requests import Request
from starlette.responses import JSONResponse

from dto.request_dto import ChatCommonRequest, ChatWithTarotCardCommonRequest
from dto.response_dto import ChatGraphResponse
from llm.chat_graph import get_chat_graph
from llm.model import llm_classify_chat, llm_reply_general_chat, llm_reply_tarot_chat, llm_reply_inappropriate_chat, \
    llm_reply_question_chat
from scheduler.history_scheduler import scheduler


@asynccontextmanager
async def lifespan(_app):
    scheduler.start()
    yield


app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False}, lifespan=lifespan)


@app.exception_handler(Exception)
async def validation_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "message": (
                f"Failed method {request.method} at URL {request.url}."
                f" Exception message is {exc!r}."
            )
        },
    )


chat_graph = get_chat_graph()


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


@app.post("/api/v1/reply/question-chat")
def reply_question_chat(req: ChatCommonRequest):
    return llm_reply_question_chat(
        question=req.chat,
        chat_room_id=req.chat_room_id
    )


@app.post("/api/v1/reply/tarot-chat")
def reply_tarot_chat(req: ChatWithTarotCardCommonRequest):
    return llm_reply_tarot_chat(
        chat_room_id=req.chat_room_id,
        tarot_card=req.tarot_card
    )


@app.post("/api/v1/reply/inappropriate-chat")
def reply_tarot_chat(req: ChatCommonRequest):
    return llm_reply_inappropriate_chat(
        question=req.chat,
        chat_room_id=req.chat_room_id
    )


@app.post("/api/v1/chat")
def chat_with_graph(req: ChatCommonRequest):
    result = chat_graph.invoke({
        "user_chat": req.chat,
        "user_room_id": req.chat_room_id
    })
    classification = result["classification"]
    answer = result["ai_chat"] if "ai_chat" in result else "ERROR"
    return ChatGraphResponse(classification=classification, answer=answer)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
