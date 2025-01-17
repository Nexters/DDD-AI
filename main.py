from fastapi import FastAPI, Response

from dto.request_dto import ChatCommonRequest

app = FastAPI()


@app.get("/health_check")
def health_check():
    return Response(status_code=200)


@app.post("/api/v1/classify/chat")
def classify_chat(req: ChatCommonRequest):
    pass


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
