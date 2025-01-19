from fastapi import FastAPI, Response

from dto.request_dto import ChatCommonRequest
from llm.model import llm_classify_chat, llm_reply_general_chat

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False})


@app.get("/health_check")
def health_check():
    return Response(status_code=200)


@app.post("/api/v1/classify/chat")
def classify_chat(req: ChatCommonRequest):
    return llm_classify_chat(req.chat)


@app.post("/api/v1/reply/general-chat")
def reply_general_chat(req: ChatCommonRequest):
    return llm_reply_general_chat(req.chat)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
