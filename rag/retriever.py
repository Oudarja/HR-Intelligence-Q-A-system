# rag/retriever.py
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

def retrieve_context(query, k=3):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    query_embedding = model.encode([query])[0]

    # Load FAISS index
    index = faiss.read_index("rag/vector_store.faiss")

    # Load document chunks
    with open("rag/doc_chunks.txt", "r") as f:
        chunks = f.read().split("\n---\n")

    # Perform similarity search
    D, I = index.search(np.array([query_embedding]), k)
    results = [chunks[i] for i in I[0] if i < len(chunks)]

    return "\n\n".join(results)
