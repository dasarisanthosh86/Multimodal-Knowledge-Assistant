import os
import mysql.connector
from dotenv import load_dotenv
import json

# ✅ Load environment variables from .env
load_dotenv()

def get_connection():
    """Create and return a MySQL connection using .env variables."""
    try:
        conn = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "127.0.0.1"),  # force TCP instead of pipe
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", ""),
            database=os.getenv("MYSQL_DATABASE", "multimodal_db"),
            connection_timeout=10
        )
        if conn.is_connected():
            print("✅ Connected to MySQL successfully.")
            return conn
    except mysql.connector.Error as e:
        print(f"❌ Error connecting to MySQL: {e}")
        return None


def insert_document(doc_id, text):
    """Insert a document into the documents table."""
    conn = get_connection()
    if conn is None:
        print("❌ No DB connection for insert_document()")
        return
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id INT AUTO_INCREMENT PRIMARY KEY,
                doc_id VARCHAR(255),
                content LONGTEXT
            )
        """)
        cursor.execute(
            "INSERT INTO documents (doc_id, content) VALUES (%s, %s)",
            (doc_id, text)
        )
        conn.commit()
        cursor.close()
        conn.close()
        print(f"✅ Document '{doc_id}' inserted successfully.")
    except Exception as e:
        print(f"❌ Failed to insert document: {e}")


def insert_embedding(document_id, chunk_index, text_chunk, embedding):
    """Insert an embedding and its text chunk into MySQL."""
    conn = get_connection()
    if conn is None:
        print("❌ No DB connection for insert_embedding()")
        return
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS embeddings (
                id INT AUTO_INCREMENT PRIMARY KEY,
                document_id VARCHAR(255),
                chunk_index INT,
                text_chunk LONGTEXT,
                embedding JSON
            )
        """)
        cursor.execute(
            "INSERT INTO embeddings (document_id, chunk_index, text_chunk, embedding) VALUES (%s, %s, %s, %s)",
            (document_id, chunk_index, text_chunk, json.dumps(embedding))
        )
        conn.commit()
        cursor.close()
        conn.close()
        print(f"✅ Inserted embedding chunk {chunk_index} for document '{document_id}'")
    except Exception as e:
        print(f"❌ Failed to insert embedding: {e}")
