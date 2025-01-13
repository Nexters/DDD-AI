from fastapi import FastAPI, Response

app = FastAPI()

@app.get("/health_check")
def health_check():
    return Response(status_code=200)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
