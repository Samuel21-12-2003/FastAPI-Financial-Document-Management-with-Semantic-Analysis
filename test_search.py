import os
from app.services import rag_service

if __name__ == "__main__":
    try:
        print("Starting local cross-encoder search test...")
        results = rag_service.semantic_search_with_reranking("What was the key financial risk", top_k=5)
        print("Search succeeded! Results:", len(results))
    except Exception as e:
        print(f"Error during search: {e}")
