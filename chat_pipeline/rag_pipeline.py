from fastapi import APIRouter
from pydantic import BaseModel
from ingestion.document_ingestion import pc
from google import genai
from chat_pipeline.llm_answerer import llm_answerer_obj

class UserQuery(BaseModel):
    text: str


rag_router = APIRouter()

# creating the client to make llm respond
client = genai.Client()


class RAGPipeline:
    def __init__(self) -> None:
        pass

    def  ragAnswer(self, text:str, embedding, chat_history:list[str], search_type: str):
        try:
            index = pc.Index(f"rag-index-{search_type}")
            result = index.query(top_k=1, vector=embedding.tolist(), include_metadata=True)
            content = result["matches"][0]["metadata"]["text_chunk"]  # type:ignore
            print(result["matches"][0]["score"])  # type:ignore

            llm_response = llm_answerer_obj.llmAnswer(question=text, context=content, chat_history=chat_history)

            return llm_response

        except Exception as e:
            print("Error:", e)
            raise ValueError(f"Unable to query Pinecone: {e}")

rag_obj = RAGPipeline()