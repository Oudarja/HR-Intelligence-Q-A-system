from sentence_transformers import SentenceTransformer
import faiss
import os

def embed_schema():
    """_summary_ : Reads that schema → generates embeddings using SentenceTransformer
        Stores it in rag/vector_store.faiss + saves doc chunks
        These steps prepare the knowledge base (RAG store) — but are not yet integrated
        with your query.
    """    
    model = SentenceTransformer("all-MiniLM-L6-v2")
    
    with open("rag/db_schema.md", "r") as f:
        schema_text = f.read()

    # Split into sections per table
    docs = schema_text.split("\n\n")
    embeddings = model.encode(docs)

    index = faiss.IndexFlatL2(len(embeddings[0]))
    index.add(embeddings)

    faiss.write_index(index, "rag/vector_store.faiss")

    with open("rag/doc_chunks.txt", "w") as f:
        for doc in docs:
            f.write(doc.strip() + "\n---\n")

    print("[✅] Embeddings created and stored in rag/vector_store.faiss")
