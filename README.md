# 📄 PDF Q&A Assistant

An intelligent document assistant that lets you upload any PDF and ask context-based questions. It uses local embeddings with FAISS and a Groq-powered LLM (e.g., LLaMA 3) to return accurate answers from your document — and only from your document.

> ⚠️ If the answer is not present in the PDF, the assistant will respond:
> _"The answer is not in the document."_

---

## 🔧 Features

- ✅ Upload any PDF document
- 🧠 Automatically chunk and embed the text using `HuggingFaceEmbeddings`
- 📚 Store embeddings locally using `FAISS`
- 💬 Query with a custom prompt using LLaMA (via Groq API)
- 🔍 Return answers strictly based on the uploaded PDF content
- 📌 Source chunks shown for each answer

---

# How It Works
**Ingestion (ingest.py)**

Loads PDF using PyPDFLoader

Splits into overlapping chunks with RecursiveCharacterTextSplitter

Embeds the chunks using HuggingFaceEmbeddings

Saves the vector store locally with FAISS

**Q&A Chain (qa_chain.py)**

Loads vector store and retrieves relevant chunks

Queries the LLaMA model (via Groq API) with a strict context-based prompt

**Streamlit App (app.py)**

Handles file upload, vector store creation, and interactive Q&A


# Example Use Cases
GATE/UPSC/Exam syllabus PDFs

Legal or policy documents

Research papers

Technical documentation




