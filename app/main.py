from fastapi import FastAPI
from app.routes.search import router as search_router
from app.routes.chat import router as chat_router

app = FastAPI(title="Real Estate Assistant API")

app.include_router(search_router)
app.include_router(chat_router)

@app.get("/")
def root():
    return {"status": "API running"}