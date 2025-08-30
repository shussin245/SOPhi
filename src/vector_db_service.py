from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from typing import List
import ollama

from config import VECTOR_DB_PATH, OLLAMA_BASE_URL, OLLAMA_MODEL_EMBEDDING

def get_embedding_model() -> OllamaEmbeddings:
    print(f"Checking for Ollama embedding model '{OLLAMA_MODEL_EMBEDDING}'...")
    try:
        response = ollama.list()
        models = response.get('models', response)  #works if it's either dict or list
        model_names = [m.get('name', m) for m in models]
        if f"{OLLAMA_MODEL_EMBEDDING}:latest" not in model_names:
            print(f"Embedding model '{OLLAMA_MODEL_EMBEDDING}' not found. Pulling it now...")
            ollama.pull(OLLAMA_MODEL_EMBEDDING)
        print(f"Embedding model '{OLLAMA_MODEL_EMBEDDING}' is ready.")
    except Exception as e:
        print(f"Error ensuring Ollama embedding model is ready: {e}")
        print("Please ensure the Ollama server is running. Exiting.")
        exit(1)

    return OllamaEmbeddings(
        base_url=OLLAMA_BASE_URL,
        model=OLLAMA_MODEL_EMBEDDING
    )

def get_vector_store() -> Chroma:
    embeddings = get_embedding_model()
    vector_store = Chroma(
        persist_directory=VECTOR_DB_PATH,
        embedding_function=embeddings
    )
    return vector_store

def add_documents_to_vector_store(docs: List[Document]):
    vector_store = get_vector_store()
    vector_store.add_documents(docs)
    vector_store.persist()
    print(f"Added {len(docs)} documents to the vector store.")

def retrieve_relevant_docs(query: str, k: int = 5) -> List[Document]:
    vector_store = get_vector_store()
    return vector_store.similarity_search(query, k=k)