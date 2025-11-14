import os
from fastapi import APIRouter, UploadFile, Query
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
from ingestion.chunking import chunkingObj
from enum import Enum

model = SentenceTransformer("all-MiniLM-L6-v2")
doc_router = APIRouter()

load_dotenv()
pc = Pinecone(api_key=os.getenv("api_key"))
index_name_fixed = "rag-index-fixed"
index_name_semantic = "rag-index-semantic"


class ChunkType(str, Enum):
    fixed = "fixed"
    semantic = "semantic"


def check_or_create_index(index_name: str):
    if not pc.has_index(index_name):
        pc.create_index(
            name=index_name,
            dimension=384,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )


check_or_create_index(index_name_fixed)
check_or_create_index(index_name_semantic)


@doc_router.post("/ingest")
async def document_ingest(
    file: UploadFile,
    chunk_type: ChunkType 
):

    vector_embedding_list = []

    # Extract text
    if file.content_type == "application/pdf":
        reader = PdfReader(file.file)
        text = "".join([page.extract_text() or "" for page in reader.pages])
    elif file.content_type == "text/plain":
        raw_text = (await file.read()).decode("utf-8")
        text = raw_text
    else:
        return {"error": "Unsupported file type"}

    if chunk_type == "fixed":
        index = pc.Index(
            index_name_fixed
        )  # this helps to index the vector DB for fixed index
        chunk_list = chunkingObj.fixedChunking(text=text)
    elif chunk_type == "semantic":
        index = pc.Index(
            index_name_semantic
        )  # this helps to index the vector DB for semantic index
        chunk_list = chunkingObj.semanticChunking(text=text)

    # Create embeddings and upsert
    embeddings = model.encode(chunk_list)
    for i, chunk in enumerate(chunk_list):
        vector_embedding_list.append(
            {
                "id": f"{file.filename}_{chunk_type}_{i}",
                "values": embeddings[i].tolist(),
                "metadata": {"chunk_type": chunk_type, "text_chunk": chunk},
            }
        )

    index.upsert(vectors=vector_embedding_list)
    return {"message": f"{chunk_type.capitalize()} chunks stored successfully"}
