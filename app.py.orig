import streamlit as st
import os
from backend.store_data import process_and_store
from backend.query_handler import generate_answer

# ================= PAGE SETTINGS =================
st.set_page_config(
    page_title="📚 Multimodal Knowledge Assistant",
    page_icon="🧠",
    layout="wide"
)

# ================= CUSTOM STYLES =================
st.markdown("""
    <style>
    body {
        background-color: #f8f9fa;
        font-family: 'Segoe UI', sans-serif;
    }
    .main-title {
        text-align: center;
        font-size: 38px;
        font-weight: 800;
        color: #222;
        margin-bottom: 5px;
    }
    .subtitle {
        text-align: center;
        font-size: 16px;
        color: #555;
        margin-bottom: 30px;
    }
    .section {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 30px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        margin-bottom: 35px;
    }
    .stButton>button {
        background-color: #0d6efd !important;
        color: white !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        border: none;
        padding: 8px 20px !important;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #0b5ed7 !important;
        transform: scale(1.03);
    }
    .footer {
        text-align: center;
        color: #777;
        font-size: 14px;
        margin-top: 40px;
    }
    </style>
""", unsafe_allow_html=True)

# ================= SIDEBAR =================
st.sidebar.title("🧭 Navigation")
menu = st.sidebar.radio("Go to", ["🏠 Home", "📂 Upload File", "🔍 Ask a Question", "ℹ️ About"])

# ================= HOME =================
if menu == "🏠 Home":
    st.markdown("<div class='main-title'>🧠 Multimodal Knowledge Assistant</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Upload any file — text, image, video, or audio — and ask intelligent questions about its content.</div>", unsafe_allow_html=True)

    st.markdown("""
    ### 💡 What You Can Do:
    - 📄 Upload PDFs, Word, PowerPoint, or text files  
    - 🖼️ Upload images (OCR coming soon)  
    - 🎧 Upload audio or video files (speech extraction supported)  
    - 🧠 Ask natural questions about your data  

    ---
    **Built with Gemini + Streamlit + MySQL**  
    """)

# ================= UPLOAD =================
elif menu == "📂 Upload File":
    st.markdown("<div class='main-title'>📤 Upload a File</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Your data will be processed, extracted, and securely stored in the database.</div>", unsafe_allow_html=True)

    st.markdown("<div class='section'>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Choose a document, image, audio, or video",
        type=["pdf", "docx", "pptx", "txt", "md", "jpg", "png", "mp3", "mp4"]
    )

    if uploaded_file:
        os.makedirs("uploads", exist_ok=True)
        file_path = os.path.join("uploads", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        st.success(f"✅ `{uploaded_file.name}` uploaded successfully!")

        with st.spinner("Processing and storing your file..."):
            doc_id, text = process_and_store(file_path)

        if text:
            st.success("✅ File processed and stored successfully!")
            st.caption(f"Document ID: `{doc_id}`")

            with st.expander("📄 View Extracted Text"):
                st.text_area("Extracted Text (Preview)", text[:3000], height=300)
        else:
            st.error("❌ Failed to process this file. Please check backend logs.")
    st.markdown("</div>", unsafe_allow_html=True)

# ================= ASK QUESTION =================
elif menu == "🔍 Ask a Question":
    st.markdown("<div class='main-title'>🔍 Ask a Question</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Query your uploaded knowledge base using natural language.</div>", unsafe_allow_html=True)

    st.markdown("<div class='section'>", unsafe_allow_html=True)
    query = st.text_input("Enter your question below:")

    if st.button("Get Answer"):
        if not query.strip():
            st.warning("⚠️ Please enter a valid question.")
        else:
            with st.spinner("Searching and generating answer..."):
                answer = generate_answer(query)

            st.markdown("### 🧠 Gemini’s Answer:")
            st.info(answer)
    st.markdown("</div>", unsafe_allow_html=True)

# ================= ABOUT =================
elif menu == "ℹ️ About":
    st.markdown("<div class='main-title'>ℹ️ About</div>", unsafe_allow_html=True)
    st.markdown("""
    ### 🤖 Multimodal Knowledge Assistant
    This intelligent assistant can process multiple data formats:
    - Text documents (`pdf`, `docx`, `pptx`, `txt`)
    - Images (`jpg`, `png`)
    - Audio/Video (`mp3`, `mp4`)

    **Key Features:**
    - Converts uploaded files into searchable knowledge
    - Embeds data into MySQL for efficient retrieval
    - Answers natural language queries using Gemini API

    ---
    **Developer:** Dasari Santhosh  
    **Backend:** Python, Streamlit, MySQL, Gemini API  
    **Version:** 1.0.0  
    """)

# ================= FOOTER =================git branch

st.markdown("<div class='footer'>© 2025 Multimodal Knowledge Assistant</div>", unsafe_allow_html=True)
