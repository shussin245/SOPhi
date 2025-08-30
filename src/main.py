from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

from src.llm_service import generate_response_from_llm
from src.vector_db_service import retrieve_relevant_docs
from src.web_search_service import perform_web_search
from config import OLLAMA_MODEL_NAME

app = FastAPI(
    title="SOPhi: SOP AI Assistant",
    description="Generates SOPs using a local LLM (Ollama), internal knowledge base (ChromaDB), and real-time web search (SerpAPI).",
    version="1.0.0"
)

class SOPRequest(BaseModel):
    topic: str
    details: str = ""

@app.get("/")
async def root():
    return {"message": "SOP AI Assistant API is running!", "ollama_model": OLLAMA_MODEL_NAME}


@app.post("/generate_sop")
async def generate_sop(request: SOPRequest):
    try:
        print(f"Retrieving internal documents for topic: '{request.topic}'")
        search_query_for_internal = f"{request.topic} {request.details}".strip()
        internal_docs = retrieve_relevant_docs(search_query_for_internal, k=5)
        
        internal_context_parts = []
        if internal_docs:
            for i, doc in enumerate(internal_docs):
                internal_context_parts.append(f"--- Internal Document Snippet {i+1} ---\n{doc.page_content}")
            internal_context = "\n\n" + "\n\n".join(internal_context_parts)
        else:
            internal_context = "\nNo specific internal SOPs found for this topic in the knowledge base."
        
        print(f"Retrieved {len(internal_docs)} relevant internal document chunks.")

        print(f"Performing web search for: '{request.topic}'")
        web_search_query = f"SOP {request.topic} best practices {request.details}".strip()
        web_context = perform_web_search(web_search_query, num_results=3)
        
        if web_context:
            print("Found relevant external information.")
            web_context_formatted = "\n\n--- External Information (Web Search) ---\n" + web_context
        else:
            print("No relevant external information found.")
            web_context_formatted = "\n\n--- External Information (Web Search) ---\nNo relevant external information found."

        prompt_template = f"""
        You are an expert AI assistant specializing in generating detailed and practical Standard Operating Procedures (SOPs).
        Your goal is to provide clear, concise, and actionable instructions for professionals.
        Use clear headings, bullet points, and code blocks for commands where appropriate.
        Tone is professional, direct, and unambiguous, suitable for staff.
        
        Generate a comprehensive SOP for the following request.
        
        ---
        **SOP Request Topic:** {request.topic}
        **Specific Requirements/Details:** {request.details if request.details else "None provided."}
        ---

        **Internal Knowledge Base Context:**
        {internal_context}
        ---

        **Up-to-date External Information (from Web Search):**
        {web_context_formatted}
        ---

        **Instructions for SOP Generation:**
        1.  Title: Start with a clear and descriptive title for the SOP.
        2.  Purpose: Briefly state the purpose of this SOP.
        3.  Scope: Define what this SOP covers and what it does not.
        4.  Prerequisites: List any tools, access, or prior conditions required.
        5.  Steps: Provide numbered, step-by-step instructions. Be highly detailed and explicit.
        6.  Troubleshooting: Include common issues and their resolutions if applicable.

        **Generated SOP:**
        """

        print(f"Sending prompt to Ollama model '{OLLAMA_MODEL_NAME}' for generation...")
        sop_content = generate_response_from_llm(prompt_template)
        
        if "Failed to generate SOP." in sop_content:
            raise HTTPException(status_code=503, detail=sop_content)

        print("SOP generated successfully.")
        return {"sop": sop_content}

    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"An unexpected error occurred during SOP generation: {e}")
        raise HTTPException(status_code=500, detail=f"An internal server error occurred: {str(e)}")