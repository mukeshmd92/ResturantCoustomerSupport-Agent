import os
import chromadb

# Local in-memory or persisted Chroma client
client = chromadb.Client()
collection = client.get_or_create_collection(name="restaurant_policies")

def init_kb():
    if collection.count() == 0 and os.path.exists("policies.txt"):
        with open("policies.txt", "r", encoding="utf-8") as f:
            content = f.read().strip()
        
        # Split by paragraph
        sections = [s.strip() for s in content.split("\n\n") if s.strip()]
        collection.add(
            documents=sections,
            ids=[f"policy_{i}" for i in range(len(sections))]
        )

def search_policy(query: str) -> str:
    init_kb()
    results = collection.query(query_texts=[query], n_results=1)
    if results["documents"] and results["documents"][0]:
        return results["documents"][0][0]
    return "No matching documented policy found."