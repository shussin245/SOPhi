import os
import shutil
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from src.vector_db_service import get_embedding_model, get_vector_store
from config import RAW_SOP_PATH, VECTOR_DB_PATH, CHUNK_SIZE, CHUNK_OVERLAP, OLLAMA_MODEL_EMBEDDING

def load_documents_from_directory(directory: str):
    documents = []
    print(f"Loading documents from: {directory}")
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if filename.endswith(".pdf"):
            print(f"  - Loading PDF: {filename}")
            loader = PyPDFLoader(file_path)
            documents.extend(loader.load())
        elif filename.endswith(".docx"):
            print(f"  - Loading DOCX: {filename}")
            loader = Docx2txtLoader(file_path)
            documents.extend(loader.load())
        else:
            print(f"  - Skipping unsupported file: {filename}")
    return documents

def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    return text_splitter.split_documents(documents)

def main():
    #Getting embedding model (this will also check/pull the model)
    embeddings = get_embedding_model()

    #Loading and splitting the documents
    raw_documents = load_documents_from_directory(RAW_SOP_PATH)
    if not raw_documents:
        print("No documents found to process. Please add files to the data/raw_sops directory.")
        return

    docs_to_ingest = split_documents(raw_documents)
    print(f"Split {len(raw_documents)} documents into {len(docs_to_ingest)} chunks.")

    #Cleaning up existing vector store to start fresh
    if os.path.exists(VECTOR_DB_PATH):
        print("Removing old vector store to prepare for new ingestion...")
        shutil.rmtree(VECTOR_DB_PATH)

    #Creating vector store and adding the documents
    print(f"Creating vector store and storing in ChromaDB at {VECTOR_DB_PATH}...")
    vector_store = get_vector_store()
    vector_store.add_documents(docs_to_ingest)
    vector_store.persist()
    print("Ingestion complete! Vector store created successfully.")

if __name__ == "__main__":
    main()