import os
import google.generativeai as genai
from backend.db import insert_embedding
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()

# ✅ Configure Gemini Embedding Model
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Model for embeddings
EMBED_MODEL = "models/embedding-001"


def chunk_text(text, chunk_size=500):
    """
    Split long text into smaller chunks for embeddings.
    Uses word-based splitting for better context preservation.
    """
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield " ".join(words[i:i + chunk_size])


def create_embeddings(doc_id, text):
    """
    Generate embeddings for text chunks and store them in MySQL.
    """
    print(f"🔍 Creating embeddings for document: {doc_id}")

    # Safety: skip if empty text
    if not text or len(text.strip()) == 0:
        print("⚠️ Skipping empty text for embedding generation.")
        return

    try:
        for i, chunk in enumerate(chunk_text(text)):
            if not chunk.strip():
                continue

            # 🔹 Generate Gemini embedding
            result = genai.embed_content(
                model=EMBED_MODEL,
                content=chunk,
                task_type="retrieval_document"  # improves search results
            )

            embedding = result.get("embedding")
            if embedding:
                insert_embedding(doc_id, i, chunk, embedding)
                print(f"✅ Inserted embedding chunk {i} for {doc_id}")
            else:
                print(f"⚠️ Empty embedding returned for chunk {i}")

        print(f"✅ All embeddings stored for document: {doc_id}")

    except Exception as e:
        print(f"❌ Embedding generation failed for {doc_id}: {e}")
