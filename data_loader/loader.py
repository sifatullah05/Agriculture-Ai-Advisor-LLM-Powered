from langchain_community.document_loaders import DirectoryLoader,PyPDFLoader

def load_pdf_data(data):
    loader = DirectoryLoader(
        data,
        glob ="*.pdf",
        loader_cls=PyPDFLoader
    )
    documents = loader.load()
    return documents