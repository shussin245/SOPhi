from serpapi import GoogleSearch
from config import SERPAPI_API_KEY
import os

def perform_web_search(query: str, num_results: int = 5) -> str:
    if not SERPAPI_API_KEY:
        print("SERPAPI_API_KEY is not set in config.py or .env file.")
        return "Web search is unavailable due to missing API key."

    try:
        params = {
            "api_key": SERPAPI_API_KEY,
            "engine": "google",
            "q": query,
            "num": num_results,
        }
        
        search = GoogleSearch(params)
        results = search.get_dict()
        organic_results = results.get("organic_results", [])
        snippets = [r.get("snippet") for r in organic_results if r.get("snippet")]
        
        if not snippets:
            print(f"No useful snippets found for query: '{query}'")
            return ""

        return "\n".join(snippets)
    except Exception as e:
        print(f"Error performing web search with SerpAPI for query '{query}': {e}")
        return f"Failed to retrieve external information for '{query}' due to an error."