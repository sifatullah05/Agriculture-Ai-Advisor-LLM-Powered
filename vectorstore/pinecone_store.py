from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from config import PINECONE_API_KEY, INDEX_NAME, EMBEDDING_DIMENSION

def initialize_vectorstore(embedding):
    pc = Pinecone(api_key=PINECONE_API_KEY)

    if not pc.has_index(INDEX_NAME):
        pc.create_index(
            name=INDEX_NAME,
            dimension=EMBEDDING_DIMENSION,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )

    vectorstore =  PineconeVectorStore.from_existing_index(
        index_name=INDEX_NAME,
        embedding=embedding
    )
    return vectorstore
