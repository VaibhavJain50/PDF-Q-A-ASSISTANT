from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv
load_dotenv()

def load_qa_chain(db_dir="vectorstore/"):
    # Load embeddings and vector store
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectordb = FAISS.load_local(db_dir, embeddings, allow_dangerous_deserialization=True)

    # Initialize Groq LLM
    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.1-8b-instant"
    )

    # Define strict prompt
    prompt_template = PromptTemplate(
        input_variables=["context", "question"],
        template="""
You are an intelligent assistant answering questions based ONLY on the following context:

{context}

Question: {question}

Answer only using the context. If the answer is not in the context, respond with:
"The answer is not in the document."
"""
    )

    # Create QA chain with the custom prompt
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectordb.as_retriever(),
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt_template}
    )

    return qa_chain
