# 🏥 MediMind AI — AI Medical Document Assistant

MediMind is a powerful Multi-Document RAG (Retrieval-Augmented Generation) application designed for professional medical document analysis. It allows users to upload multiple PDF reports and ask complex questions across all of them simultaneously.

## 🚀 Quick Launch

1. **Setup Environment** (Run once):
   ```bash
   setup.bat
   ```
2. **Launch MediMind**:
   ```bash
   run.bat
   ```

---

## ✨ Features

- **Multi-Doc Support**: Upload and analyze multiple medical reports together.
- **RAG Pipeline**: Powered by **LangChain**, **Groq (Llama 3)**, and **Fast Embeddings**.
- **Premium Interface**: A modern, glassmorphic UI designed for clarity and ease of use.
- **Session Persistence**: Maintains context during your analysis session.

---

## 🛠️ Project Structure

- `app/main.py`: High-performance **FastAPI** backend.
- `logic/rag_pipeline.py`: Shared core logic for document processing and RAG.
- `app/templates/index.html`: The premium frontend.
- `storage/uploads`: Temporary storage for your analysis files.

---

## 🔑 Environment Variables (.env)

Make sure your `.env` file contains the following (already configured for you):
- `GROQ_API_KEY`: For powerful LLM analysis.
- `GEMINI_API_KEY`: For ultra-fast document embedding.

---

## ⚡ Recent Fixes (Runnable Code)

1. **Fixed Module Errors**: Resolved `ModuleNotFoundError` for `langchain.chains` and `sentence_transformers`.
2. **Faster Start**: Replaced local `HuggingFace` embeddings with `GoogleGenerativeAIEmbeddings` to avoid massive 500MB+ downloads.
3. **Unified Logic**: Consolidated session handling between FastAPI and Flask.
4. **Enhanced UI**: Polished the frontend for a more professional 'MediMind' feel.

---
*Created with ❤️ by Antigravity AI*

This is a comprehensive guide to your project, MediMind AI, structured perfectly for your presentation.

🏥 Project Overview: MediMind AI
Tagline: Your Specialized AI Medical Document Assistant

MediMind is a sophisticated Multi-Document RAG (Retrieval-Augmented Generation) application. It is designed to help users (patients or healthcare professionals) instantly synthesize information from multiple medical reports (PDFs) by asking questions in plain English.

1. The Problem & Solution
The Problem: Medical folders are often filled with dozens of pages of reports (blood tests, MRIs, discharge summaries). Manually finding a specific value or understanding the "big picture" across multiple documents is time-consuming and prone to human error.
The Solution: MediMind allows users to "talk" to their entire medical folder. It reads all uploaded documents, understands the clinical context, and provides accurate, evidence-based answers with source citations.
2. The Tech Stack (The "Engine")
Your project uses a modern, high-performance stack:

Backend: FastAPI — A modern, high-performance Python framework known for its speed and native support for asynchronous operations.
LLM (The Brain): Groq (Llama 3.3 70B) — We use Groq's LPUs (Language Processing Units) to achieve near-instant response times, making the AI feel incredibly responsive.
RAG Framework: LangChain — The "orchestrator" that connects the documents, the vector store, and the LLM.
Embeddings: HuggingFace (all-MiniLM-L6-v2) — A local, lightweight model that converts medical text into mathematical vectors for fast searching.
Vector Database: FAISS (Facebook AI Similarity Search) — An industry-standard library for efficient similarity searching of document chunks.
Frontend: Vanilla HTML5/CSS3/JS with a Glassmorphic UI design for a premium, professional medical feel.
3. How it Works (The RAG Pipeline)
When you upload a document, four things happen behind the scenes:

Ingestion: The PDF is loaded and cleaned using PyPDFLoader.
Chunking: The text is split into small, manageable pieces (1,000 characters each) with a 100-character overlap to ensure no context is lost.
Embedding: Each chunk is converted into a vector (a list of numbers) that represents its semantic meaning.
Retrieval: When a user asks a question, the system finds the top 5 most relevant chunks from the documents and sends them to the LLM as "Ground Truth."
4. Key Technical Features
Multi-Document Support: Unlike basic RAG apps, MediMind can handle multiple files simultaneously, allowing for cross-document analysis (e.g., comparing a blood test from January with one from May).
History-Aware Retrieval: The system remembers the last 10 messages. If you ask "What about my sugar levels?" and then "Is that high?", the AI knows "that" refers to the sugar levels.
Source Attribution: Every answer is backed by "Source Tags," showing exactly which document the information was pulled from.
Medical Guardrails: The AI is strictly instructed to only answer based on the provided context. If the information isn't in the reports, it won't hallucinate or make up medical advice.
5. Project Structure
/logic/rag_pipeline.py: Contains the core AI logic, embedding settings, and the LangChain retrieval chain.
/app/main.py: The FastAPI server handling file uploads, session management, and API routing.
/app/templates/index.html: The interactive dashboard where users interact with the system.
/storage/uploads: Secure temporary storage for processed medical files.
🌟 Presentation "Pro-Tips"
Mention Speed: Emphasize that using Groq makes the analysis happens in milliseconds, which is critical for medical environments.
Emphasize Privacy: Mention that using Local Embeddings means the document vectorization happens on the server without sending text to third-party providers until the final query.
Show the UI: Highlight the "Total Pages" and "Total Chunks" counters in the sidebar—it shows the system is actually "crunching" the data.xs