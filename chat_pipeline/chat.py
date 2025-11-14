import os

from fastapi import APIRouter
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from ingestion.document_ingestion import pc, model
from google import genai
from chat_pipeline.llm_answerer import llm_answerer_obj
from chat_pipeline.decisive import decisiveObj
from chat_pipeline.chat_history import chathistoryobj

from dotenv import load_dotenv

load_dotenv()


class UserQuery(BaseModel):
    text: str
    userid: int
    search_type: str= 'fixed' or 'semantic'


rag_router = APIRouter()

# creating the client to make llm respond
client = genai.Client()
history_list = []


@rag_router.post("/chat")
async def Chat(request: UserQuery):
    text = request.text
    userid = request.userid
    search_type = request.search_type
    print(userid)
    embedding = model.encode(text)

    # retrieving the chat history if any for the specific user
    history_list = chathistoryobj.retriveChatHistory(userid)

    # to decide the path:- booking or question answering
    response = decisiveObj.decideIntent(question=text, embedding=embedding, chat_history=history_list, search_type=search_type)
    chat_history_list = [{"role": "user", "text": text}, {"role": "llm", "text": response}]

    # to store the conversation immediately as the response arrives
    chathistoryobj.storeChatHistory(userid,chat_history_list)

    return response
