from sentence_transformers import SentenceTransformer
from backend.db import insert_embedding

model = SentenceTransformer('all-MiniLM-L6-v2')  # Fast, reliable

def chunk_text(text, chunk_size=500):
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield " ".join(words[i:i + chunk_size])

def create_embeddings(doc_id, text):
    print(f"🔍 Creating embeddings for document: {doc_id}")
    try:
        for i, chunk in enumerate(chunk_text(text)):
            embedding = model.encode(chunk).tolist()
            insert_embedding(doc_id, i, chunk, embedding)
        print(f"✅ All embeddings stored for {doc_id}")
    except Exception as e:
        print(f"❌ Embedding generation failed: {e}")
