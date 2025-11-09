import os
import google.generativeai as genai
from dotenv import load_dotenv
from backend.search_engine import search_similar_chunks

# ✅ Load .env variables
load_dotenv()

# ✅ Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def generate_answer(query: str) -> str:
    """
    Uses Gemini to generate an answer from the database context.
    """
    # 1️⃣ Find relevant chunks
    similar_chunks = search_similar_chunks(query, top_k=5)

    if not similar_chunks:
        return "⚠️ No relevant data found in the database."

    # 2️⃣ Prepare context from retrieved chunks
    context = "\n\n".join([chunk[2] for chunk in similar_chunks])

    # 3️⃣ Send to Gemini
    try:
        prompt = f"""
        You are a helpful assistant. Use the following document context to answer the user query.

        Context:
        {context}

        User Query:
        {query}

        Provide a clear, accurate, and concise answer.
        """

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        return response.text.strip()

    except Exception as e:
        return f"❌ Gemini error: {e}"
