from pathlib import Path
from PyPDF2 import PdfReader
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


def get_embeddings(embedding_provider, model_name: str):
    """create embeddings

    Args:
        embedding_provider: Use embedding providers like Hugging face/ Open Ai
        model_name (str): model name for embedding

    Returns:
        specific embedding instance
    """
    return embedding_provider(model_name=model_name)


def get_vectorstore_from_document(vector_store, embeddings, text_chunks: list):
    """ generate vector stores

    Args:
        text_chunks (list): chunks needed to convert to embeddings

    Returns: vector store with embedding
    """

    vector_stores = vector_store.from_documents(documents=text_chunks,
                                                embedding=embeddings)
    return vector_stores


def get_document_chunks(documents) -> list:
    """

    Args:
        documents: pdf documents text needed to converted to chunks

    Returns:
        list: list chunks created using spitting criteria
    """

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=50)

    chunks = text_splitter.split_documents(documents)

    return chunks


def pdf_reader(path: Path) -> str:
    """ 
    Args:
        path :pdf file path
    Returns
        str: string contains all pdf text
    """
    text = ""
    pdf_reader = PdfReader(path)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


def document_loader(document_path: Path):
    """load documents

    Keyword arguments:
    document path  -- directory which contains pdf documents
    Return: pdf files converted to Documents
    """

    loader = DirectoryLoader(document_path)
    documents = loader.load()
    return documents
