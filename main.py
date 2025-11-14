from fastapi import FastAPI, APIRouter
from ingestion.document_ingestion import doc_router
from chat_pipeline.chat import rag_router
from database import init_db

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Run on startup
    init_db()
    yield
    # Optional: shutdown tasks
    print("App shutting down...")


app = FastAPI(lifespan=lifespan)


app.include_router(router=doc_router)
app.include_router(router=rag_router)
