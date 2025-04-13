from fastapi import APIRouter

app = APIRouter()


@app.get("/")
def health():
    return {"status": "ok"}
