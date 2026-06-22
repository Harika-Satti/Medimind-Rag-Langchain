import os
import torch
import uuid
import logging
import sys
from typing import Optional, Dict, Annotated

# -- Fix for OpenMP / shm.dll initialization error --
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from fastapi import FastAPI, UploadFile, File, HTTPException, Body, Form
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from starlette.requests import Request

# -- Path Fix --
# Add parent dir to path so we can import 'logic' from anywhere
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

try:
    from logic.rag_pipeline import get_rag_chain, embeddings, process_pdf
    from langchain_core.messages import HumanMessage, AIMessage
    from langchain_community.vectorstores import FAISS
except ImportError as e:
    print(f"❌ CRITICAL ERROR: Could not import MediMind logic. {e}")
    # Define placeholder to allow starting app (will error on use)
    embeddings = None
    process_pdf = None
    get_rag_chain = None

# -- Setup --
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="MediMind — AI Medical Document Assistant")

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version="1.0.0",
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["openapi"] = "3.0.3"
    
    # Fix the 3.1 -> 3.0 schema conversion for file uploads
    # This ensures Swagger UI shows a file picker instead of a text box
    for _, schema in openapi_schema.get("components", {}).get("schemas", {}).items():
        if "properties" in schema:
            for prop_name, prop_data in schema["properties"].items():
                # Handle single file or array of files
                if prop_data.get("type") == "array" and "items" in prop_data:
                    if prop_data["items"].get("contentMediaType") == "application/octet-stream":
                        prop_data["items"]["type"] = "string"
                        prop_data["items"]["format"] = "binary"
                        del prop_data["items"]["contentMediaType"]
                elif prop_data.get("contentMediaType") == "application/octet-stream":
                    prop_data["type"] = "string"
                    prop_data["format"] = "binary"
                    del prop_data["contentMediaType"]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Folders
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "storage", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Templates
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

# -- State --
sessions: Dict[str, dict] = {}

# -- API Routes --

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("fastapi_index.html", {"request": request})

@app.post("/upload")
async def upload_pdf(
    files: Annotated[list[UploadFile], File(description="Multiple PDF files")], 
    session_id: Annotated[str | None, Form()] = None
):
    if not session_id or session_id == "null":
        session_id = str(uuid.uuid4())[:8]

    uploaded_results = []
    
    try:
        for file in files:
            if not file.filename.lower().endswith(".pdf"):
                continue

            file_path = os.path.join(UPLOAD_DIR, f"{session_id}_{file.filename}")
            with open(file_path, "wb") as f:
                f.write(await file.read())

            # Process docs via shared logic
            documents, chunks = process_pdf(file_path, file.filename)

            # Update or create Vectorstore
            if session_id in sessions:
                sessions[session_id]["vs"].add_documents(chunks)
                sessions[session_id]["docs"].append(file.filename)
                sessions[session_id]["pages"] += len(documents)
                sessions[session_id]["chunks"] += len(chunks)
            else:
                vs = FAISS.from_documents(chunks, embeddings)
                sessions[session_id] = {
                    "vs": vs,
                    "history": [],
                    "docs": [file.filename],
                    "pages": len(documents),
                    "chunks": len(chunks)
                }
            
            uploaded_results.append(file.filename)

        if not uploaded_results:
            raise HTTPException(status_code=400, detail="No valid PDF files were uploaded.")

        return {
            "session_id": session_id,
            "filename": ", ".join(uploaded_results),
            "all_docs": sessions[session_id]["docs"],
            "pages": sessions[session_id]["pages"],
            "chunks": sessions[session_id]["chunks"]
        }
    except Exception as e:
        logger.error(f"Upload error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask")
async def ask_question(
    query: str = Body(..., embed=True),
    doc_name: str = Body(..., embed=True),
    model: Optional[str] = Body(None, embed=True)
):
    session_id = doc_name
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Analysis session not found. Please re-upload documents.")

    session_data = sessions[session_id]
    vs = session_data["vs"]
    history = session_data["history"]

    try:
        rag_chain = get_rag_chain(vs)
        response = rag_chain.invoke({"input": query, "chat_history": history})

        # Track history
        history.append(HumanMessage(content=query))
        history.append(AIMessage(content=response["answer"]))
        if len(history) > 10:
            session_data["history"] = history[-10:]

        # Extract sources from response
        sources = [{"content": doc.page_content, "file": doc.metadata.get("source", "Medical Record")} for doc in response["context"]]

        return {
            "answer": response["answer"],
            "sources": sources,
            "model": "Multi-Doc Engine (MediMind)"
        }
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Analysis error: {error_msg}")
        
        # User-friendly messages for common API issues
        if "401" in error_msg or "invalid_api_key" in error_msg:
            detail = "Invalid Groq API Key detected in the source code. Please verify your hardcoded key."
        elif "rate_limit_exceeded" in error_msg:
            detail = "Rate limit reached for Groq API. Please wait a moment."
        else:
            detail = f"Analysis Error: {error_msg}"
            
        raise HTTPException(status_code=500, detail=detail)

@app.post("/clear")
async def clear_session():
    sessions.clear()
    return {"ok": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
