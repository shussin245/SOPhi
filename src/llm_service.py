import ollama
from config import OLLAMA_BASE_URL, OLLAMA_MODEL_NAME

def generate_response_from_llm(prompt: str) -> str:
    try:
        client = ollama.Client(host=OLLAMA_BASE_URL)
        response = client.chat(
            model=OLLAMA_MODEL_NAME,
            messages=[{'role': 'user', 'content': prompt}],
            options={
                "temperature": 0.5,
                "top_k": 40,
                "top_p": 0.9
            }
        )
        return response['message']['content']
    except Exception as e:
        print(f"Error calling local LLM at {OLLAMA_BASE_URL} with model {OLLAMA_MODEL_NAME}: {e}")
        return "Failed to generate SOP. Please ensure the Ollama server is running and the model is available."