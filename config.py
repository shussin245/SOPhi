import os
from dotenv import load_dotenv

load_dotenv()

RAW_SOP_PATH = "data/raw_sops/"
VECTOR_DB_PATH = "data/embeddings/chroma/"

SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL_NAME = "mistral"
OLLAMA_MODEL_EMBEDDING = "nomic-embed-text"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100