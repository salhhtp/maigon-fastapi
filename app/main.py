# app/main.py
from fastapi import FastAPI
from app.config import settings
from app.db import engine, Base
from app.routers import auth, documents, reviews, subscriptions, webhooks
import uvicorn

app = FastAPI(title="Maigon API - Sprint 1", version="0.1")

# include routers
app.include_router(auth.router)
app.include_router(documents.router)
app.include_router(reviews.router)
app.include_router(subscriptions.router)
app.include_router(webhooks.router)

@app.on_event("startup")
async def startup_event():
    # You can optionally create tables here if you want auto-create on startup (not recommended for prod)
    # But for dev/demo, let's create tables if they don't exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/health")
async def health():
    return {"status": "ok"}
