def get_retriever(vectorstore,namespace=None):
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": 3,
            "namespace": namespace
        }
    )
    return retriever
    
    
