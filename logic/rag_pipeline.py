import os
import logging
from dotenv import load_dotenv

# LangChain & RAG Imports
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq

# ✅ Standard RAG Imports
from langchain_classic.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

# -- Setup --

load_dotenv()
logger = logging.getLogger(__name__)

# -- Models --

def get_llm():
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        logger.error("❌ GROQ_API_KEY is missing in .env file.")
        raise ValueError("GROQ_API_KEY missing. Please add it to your .env file.")
    
    return ChatGroq(
        api_key=api_key,
        model_name="llama-3.3-70b-versatile",
        temperature=0.1
    )

# Using local embeddings (MiniLM) for zero-latency, private, and free vectorization
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def get_rag_chain(vectorstore):
    llm = get_llm()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    # Contextualize Question
    contextualize_q_system_prompt = (
        "Given a chat history and the latest user question "
        "which might reference context in the chat history, "
        "formulate a standalone question which can be understood "
        "without the chat history."
    )
    contextualize_q_prompt = ChatPromptTemplate.from_messages([
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])
    history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)

    # Answer question
    system_prompt = (
        "You are MediMind, a specialized medical document assistant. "
        "Strictly only use the following pieces of retrieved context from the uploaded PDF to answer the user's question. "
        "If the answer is not contained within the provided context, politely inform the user that you can only answer questions based on the uploaded documents. "
        "Do NOT use any external medical knowledge or common knowledge outside of what is provided in the text. "
        "Maintain a professional, medical tone but keep explanations clear for users."
        "\n\n"
        "{context}"
    )
    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])
    
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
    return rag_chain

def process_pdf(file_path, filename):
    """Shared PDF processing logic."""
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    for doc in documents:
        doc.metadata["source"] = filename
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(documents)
    return documents, chunks
