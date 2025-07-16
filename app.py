import streamlit as st
from ingest import create_vector_store
from qa_chain import load_qa_chain
import os

st.set_page_config(page_title="PDF QA Assistant", layout="centered")
st.title("📄 PDF Q&A Assistant")

st.markdown("""
Ask questions **strictly based on your uploaded PDF**.
If the answer is not found in the PDF, the assistant will respond:
> _"The answer is not in the document."_
""")

# Upload PDF
uploaded_file = st.file_uploader("📤 Upload a PDF file", type="pdf")

if uploaded_file:
    file_path = os.path.join("docs", uploaded_file.name)
    os.makedirs("docs", exist_ok=True)

    # Save the uploaded PDF
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    # Clear any previous responses
    st.session_state.pop("chain", None)

    with st.spinner("🔍 Processing and indexing your PDF..."):
        create_vector_store(file_path)

    st.success("✅ PDF indexed successfully!")

    # Load QA chain
    st.session_state["chain"] = load_qa_chain()

# Ask Questions
if "chain" in st.session_state:
    st.subheader("❓ Ask a Question about the PDF:")
    user_question = st.text_input("Type your question below:")

    if user_question:
        with st.spinner("🤖 Generating answer..."):
            result = st.session_state["chain"]({"query": user_question})

            st.markdown("### 💡 Answer:")
            st.write(result["result"])

            # Show source chunks
            if result.get("source_documents"):
                with st.expander("📚 Source Chunks"):
                    for i, doc in enumerate(result["source_documents"], 1):
                        st.markdown(f"**Chunk {i}:**")
                        st.write(doc.page_content[:500] + "...")
            else:
                st.info("No relevant content found in the document.")
