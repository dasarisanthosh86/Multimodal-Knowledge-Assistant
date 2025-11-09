import os
import json
import mysql.connector
import numpy as np
from dotenv import load_dotenv
import google.generativeai as genai
from backend.db import get_connection

# ✅ Load environment variables
load_dotenv()

# ✅ Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ---------- Embedding Helper ----------
def generate_query_embedding(query: str):
    """
    Generate a vector embedding for the user query using Gemini.
    """
    try:
        model = "models/embedding-001"
        response = genai.embed_content(model=model, content=query)
        return np.array(response["embedding"], dtype=np.float32)
    except Exception as e:
        print(f"❌ Error generating query embedding: {e}")
        return None


# ---------- Search Helper ----------
def fetch_all_embeddings():
    """
    Fetch all embeddings and their chunks from the MySQL database.
    """
    conn = get_connection()
    if conn is None:
        print("❌ No database connection available.")
        return []

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT document_id, chunk_index, text_chunk, embedding FROM embeddings")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        for row in rows:
            row["embedding"] = np.array(json.loads(row["embedding"]), dtype=np.float32)
        return rows
    except Exception as e:
        print(f"❌ Error fetching embeddings: {e}")
        return []


def cosine_similarity(a, b):
    """Compute cosine similarity between two vectors."""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def find_most_relevant_chunks(query_embedding, top_k=3):
    """
    Find top_k chunks most similar to the query embedding.
    """
    rows = fetch_all_embeddings()
    if not rows:
        print("⚠️ No embeddings found in the database.")
        return []

    similarities = []
    for row in rows:
        sim = cosine_similarity(query_embedding, row["embedding"])
        similarities.append((sim, row["text_chunk"]))

    similarities.sort(key=lambda x: x[0], reverse=True)
    top_chunks = [chunk for _, chunk in similarities[:top_k]]
    return top_chunks


# ---------- Answer Generation ----------
def generate_answer(query: str):
    """
    Generate a natural language answer using Gemini based on retrieved chunks.
    """
    query_embedding = generate_query_embedding(query)
    if query_embedding is None:
        return "❌ Failed to generate embedding for query."

    relevant_chunks = find_most_relevant_chunks(query_embedding)
    if not relevant_chunks:
        return "⚠️ No relevant data found in the database."

    context = "\n\n".join(relevant_chunks)

    prompt = f"""
You are an intelligent assistant. Use the context below to answer the user query accurately.

Context:
{context}

User Query:
{query}

Answer:
    """

    try:
        response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"❌ Gemini API error: {e}"
