import uuid
from data_loader.loader import load_pdf_data
from data_loader.splitter import text_split
from embeddings.embedding_model import huggingface_embedding
from vectorstore.pinecone_store import initialize_vectorstore
from config import DATA_PATH

def ingest_agriculture_data():
    """
    Ingest agriculture dataset into Pinecone using unique namespace.
    """

    kb_id = str(uuid.uuid4())

    documents = load_pdf_data(DATA_PATH)

    if not documents:
        raise ValueError("No documents found in DATA_PATH")

    chunks = text_split(documents)

    embedding = huggingface_embedding()
    vector_store = initialize_vectorstore(embedding)

    vector_store.add_documents(
        documents=chunks,
        namespace=kb_id
    )

    return {
        "knowledge_base_id": kb_id
    }

