# SOPhi: AI SOP Assistant
---

## Overview
This project is a powerful AI-powered assistant designed to streamline the creation of detailed and practical Standard Operating Procedures (SOPs). It uses a Retrieval-Augmented Generation (RAG) approach to provide highly contextual and accurate outputs.

By combining an internal knowledge base of your organization's existing SOPs with up-to-date information from the internet, the assistant generates comprehensive documents tailored to your specific needs. This ensures your SOPs are both consistent with your internal policies and current with the latest technology and best practices.

---

## Key Features
- **Local LLM Integration**: Powered by Ollama, the application uses a locally-run, quantized LLM (Mistral) for private, efficient, and cost-free text generation.  
- **Internal Knowledge Base**: Existing SOPs (PDFs, DOCX) are ingested, chunked, and stored in a local ChromaDB vector database. This allows the assistant to pull from your organization's unique policies and procedures.  
- **Real-time Web Search**: The application integrates with SerpAPI to perform real-time web searches, ensuring the generated SOPs include the latest information, security updates, and technical details.  
- **FastAPI Backend**: A robust and scalable RESTful API provides a clean interface for generating SOPs, making it easy to integrate with other applications.

---

## Directory Structure
```
SOPhi/
├── README.md                  - This file
├── .env.example               - Example file for environment variables
├── .gitignore                 - Files to be ignored by Git
├── requirements.txt           - Python dependencies
├── config.py                  - Configuration settings
├── scripts/
│   └── ingest_sops.py         - Script to process and ingest documents
├── src/
│   ├── main.py                - The core FastAPI application
│   ├── llm_service.py         - Handles communication with the local LLM
│   ├── vector_db_service.py   - Manages the ChromaDB vector store
│   ├── web_search_service.py  - Connects to the SerpAPI for web search
├── data/
│   ├── raw_sops/              - **Place your raw SOPs (PDF, DOCX) here**
│   └── embeddings/            - Local vector store data (generated)
└── examples/
    └── example_usage.py       - A script to demonstrate API usage
```

---

## Prerequisites
Before you begin, ensure you have the following installed on your system:
- Python 3.9+  
- [Ollama](https://ollama.ai) (through terminal)  
- [SerpAPI Key](https://serpapi.com/)  

---

## Getting Started

### Step 1: Clone the Repository
```bash
git clone https://github.com/shussin245/SOPhi.git
cd SOPhi
```

### Step 2: Set Up the Environment
```bash
#Create virtual environment
python3 -m venv venv

#Activate virtual environment
source venv/bin/activate  
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
Create a `.env` file in the project root:
```env
SERPAPI_API_KEY="your-serpapi-key-here"
```

You can edit the `.env.example` file provided and save as `.env`.

### Step 5: Pull the Models
```bash
#Pull the generative LLM
ollama pull mistral

#Pull the embedding model
ollama pull nomic-embed-text
```

---

## Usage Guide

### 1. Start the Ollama Server
```bash
ollama serve
```

### 2. Ingest Documents
Add SOPs to `data/raw_sops/` and run:
```bash
python -m scripts.ingest_sops
```

This creates the embeddings in `data/embeddings/`.

### 3. Run the FastAPI Server
```bash
uvicorn src.main:app --reload
```
Server runs on: [http://127.0.0.1:8000](http://127.0.0.1:8000)

### 4. Generate an SOP
In a new terminal with your virtual environment activated, run:
```bash
python examples/example_usage.py
```

---

## Technical Notes & Best Practices

### Performance
- **Ingesting SOPs**: ~10 minutes  
- **Generating SOPs**: ~20 minutes  

### Temperature
- **0** → deterministic  
- **0.3–0.7** → balanced (recommended)  
- **0.9+** → highly creative, risk of hallucinations  
Default: **0.5** for SOPs

### Embeddings
- Deterministic vectors for text  
- No seed needed for inference  
- Seeds only matter for fine-tuning/sampling tasks  

### Chunking
- Smaller chunks = better semantic precision, worse context  
- Larger chunks = better context, worse precision  
Recommended: **500 chars + 100 overlap**

---

## Next Steps
- [ ] Optimize ingestion/generation speed  
- [ ] Web UI for non-technical users
- [ ] Fine-tuned models for domain-specific SOPs  

---

## Contribution
Pull requests and issues are welcome.
