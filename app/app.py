import os
import torch
import uuid
import logging
import sys

# -- Fix for OpenMP / shm.dll initialization error --
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from flask import Flask, request, jsonify, render_template, session as flask_session
from flask_cors import CORS

# -- Path Fix --
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from logic.rag_pipeline import get_rag_chain, embeddings, process_pdf
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.vectorstores import FAISS

# -- Setup --
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), "templates"))
app.secret_key = "medimind-secret-key-gen-98765"
CORS(app)

# Folders
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "storage", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# -- State (Single Worker Mode) --
session_store = {}

# -- Routes --

@app.route("/")
def home():
    return render_template("flask_index.html")

@app.route("/upload", methods=["POST"])
def upload():
    if 'files' not in request.files:
        return jsonify({"error": "No files uploaded."}), 400
    
    files = request.files.getlist("files")
    session_id = request.form.get("session_id") or flask_session.get("session_id")

    if not session_id or session_id == "null":
        session_id = str(uuid.uuid4())[:8]
        flask_session["session_id"] = session_id

    uploaded_results = []
    
    try:
        for file in files:
            if not file.filename.lower().endswith(".pdf"):
                continue

            path = os.path.join(UPLOAD_DIR, f"{session_id}_{file.filename}")
            file.save(path)

            # Process docs via shared logic
            documents, chunks = process_pdf(path, file.filename)

            # Update Vectorstore
            if session_id in session_store:
                session_store[session_id]["vs"].add_documents(chunks)
                session_store[session_id]["docs"].append(file.filename)
                session_store[session_id]["pages"] += len(documents)
                session_store[session_id]["chunks"] += len(chunks)
            else:
                vs = FAISS.from_documents(chunks, embeddings)
                session_store[session_id] = {
                    "vs": vs,
                    "docs": [file.filename],
                    "history": [],
                    "pages": len(documents),
                    "chunks": len(chunks)
                }
            
            uploaded_results.append(file.filename)

        if not uploaded_results:
            return jsonify({"error": "No valid PDF files were uploaded."}), 400

        return jsonify({
            "session_id": session_id,
            "filename": ", ".join(uploaded_results),
            "all_docs": session_store[session_id]["docs"],
            "pages": session_store[session_id]["pages"],
            "chunks": session_store[session_id]["chunks"]
        })
    except Exception as e:
        logger.error(f"Upload error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    session_id = data.get("doc_name") or flask_session.get("session_id")
    query = data.get("query")

    if not session_id or session_id not in session_store:
        return jsonify({"error": "Session lost. Please re-upload documents."}), 404

    try:
        current_data = session_store[session_id]
        rag_chain = get_rag_chain(current_data["vs"])
        
        response = rag_chain.invoke({
            "input": query,
            "chat_history": current_data["history"]
        })

        # Track History
        current_data["history"].append(HumanMessage(content=query))
        current_data["history"].append(AIMessage(content=response["answer"]))
        current_data["history"] = current_data["history"][-10:]

        # Format sources
        sources = [{"content": doc.page_content, "file": doc.metadata.get("source", "Medical Record")} for doc in response["context"]]

        return jsonify({
            "answer": response["answer"],
            "sources": sources,
            "model": "Multi-Doc Engine (MediMind)"
        })
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Analysis error: {error_msg}")
        
        # User-friendly error for common API issues
        if "401" in error_msg or "invalid_api_key" in error_msg:
            friendly_msg = "Invalid Groq API Key detected in the source code. Please verify your hardcoded key."
        elif "rate_limit_exceeded" in error_msg:
            friendly_msg = "Rate limit reached for Groq API. Please wait a moment."
        else:
            friendly_msg = f"Analysis Error: {error_msg}"
            
        return jsonify({"error": friendly_msg}), 500

@app.route("/clear", methods=["POST"])
def clear():
    flask_session.clear()
    session_store.clear()
    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)