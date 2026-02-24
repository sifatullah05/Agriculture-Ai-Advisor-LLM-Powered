from langchain_text_splitters import RecursiveCharacterTextSplitter
def text_split(documents):
    text_split = RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)
    text_chunk = text_split.split_documents(documents)
    return text_chunk