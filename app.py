from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from ingest import ingest_agriculture_data
from embeddings.embedding_model import huggingface_embedding
from llm.groq_model import build_chat_model
from vectorstore.pinecone_store import initialize_vectorstore
from chains.prompt import SYSTEM_PROMPT
from retriever.retriever import get_retriever
from chains.rag_chain import build_rag_chain
from utils.memory import store
from config import GROQ_API_KEY
import os

app = FastAPI(title="Agriculture RAG Chatbot")

class ChatRequest(BaseModel):
    question: str
    session_id: str
    knowledge_base_id: str

embedding = huggingface_embedding()
vector_store = initialize_vectorstore(embedding)
llm = build_chat_model(GROQ_API_KEY)


@app.post("/ingest",status_code=201)
def ingest():
   try:
       result = ingest_agriculture_data()
       return {"message": "Data ingestion successful", "result": result}
   except Exception as e:
       raise HTTPException(
           status_code=500,
           detail=str(e)
       )
   
@app.post("/chat")
def chat(request: ChatRequest ):
    try:
        if not request.knowledge_base_id:
            raise HTTPException(
                status_code=400,
                detail="Knowledge base ID required"
            )
        retriever = get_retriever(
            vector_store,
            namespace = request.knowledge_base_id
        )

        rag_chain = build_rag_chain(retriever,llm)

        response = rag_chain.invoke(
            {
                "question":request.question
            },
            config = {"configurable":{"session_id":request.session_id}}
        )
        return {"answer": response}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail = str(e)
        )
    
@app.delete("/chat/{session_id}")
def delete_chat(session_id: str):
    if session_id in store:
        del store[session_id]
        return {"message": "Chat history successfully deleted"}
    raise HTTPException(
        status_code= 404,
        detail= "Session ID not found"
    )