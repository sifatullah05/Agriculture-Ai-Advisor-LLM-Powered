import os
from dotenv import load_dotenv

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY missing")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY missing")

INDEX_NAME = "agriculture-advisor"
EMBEDDING_DIMENSION = 384
DATA_PATH = "data/"
