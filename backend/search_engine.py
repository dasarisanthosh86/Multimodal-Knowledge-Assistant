import os
import numpy as np
import json
import mysql.connector
from dotenv import load_dotenv
import google.generativeai as genai
from backend.db import get_connection

# ✅ Load environment variables
load_dotenv()

# ✅ Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use Gemini embedding model
EMBED_MODEL = "models/embedding-001"


def cosine_similarity(a, b):
    """Compute cosine similarity between two embedding vectors."""
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def search_similar_chunks(query, top_k=5):
    """
    Search MySQL for chunks most similar to the query.
    """
    conn = get_connection()
    if conn is None:
        print("❌ No DB connection in search_similar_chunks()")
        return []

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, document_id, text_chunk, embedding FROM embeddings")
        results = cursor.fetchall()

        if not results:
            print("⚠️ No embeddings found in database.")
            return []

        # 1️⃣ Embed the query
        query_embedding = genai.embed_content(model=EMBED_MODEL, content=query)['embedding']

        # 2️⃣ Compute similarity for each chunk
        similarities = []
        for row in results:
            chunk_id, doc_id, text_chunk, embedding_json = row
            try:
                embedding = json.loads(embedding_json)
                score = cosine_similarity(query_embedding, embedding)
                similarities.append((chunk_id, doc_id, text_chunk, score))
            except Exception as e:
                print(f"⚠️ Error computing similarity for chunk {chunk_id}: {e}")

        # 3️⃣ Sort by similarity score (descending)
        similarities.sort(key=lambda x: x[3], reverse=True)
        return similarities[:top_k]

    except Exception as e:
        print(f"❌ Search failed: {e}")
        return []

    finally:
        cursor.close()
        conn.close()
