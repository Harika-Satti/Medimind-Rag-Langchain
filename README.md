# 🏥 MediMind AI
### *Your Specialized AI Medical Document Assistant*

> Upload multiple medical reports and instantly get accurate, evidence-based answers — powered by RAG, LangChain, and Groq's ultra-fast LPUs.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-000000?style=for-the-badge&logo=chainlink&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-F55036?style=for-the-badge&logo=groq&logoColor=white)

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [How It Works](#-how-it-works)
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [Environment Variables](#-environment-variables)
- [Contributing](#-contributing)

---

## 🧠 Overview

Medical folders are often filled with dozens of pages of reports — blood tests, MRIs, discharge summaries. Manually finding a specific value or understanding the "big picture" across multiple documents is time-consuming and error-prone.

**MediMind** solves this by letting users *talk* to their entire medical folder. It reads all uploaded PDFs, understands the clinical context, and provides accurate answers with source citations — in plain English.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📄 **Multi-Document RAG** | Upload and query multiple PDFs simultaneously |
| ⚡ **Ultra-Fast Responses** | Powered by Groq LPUs for near-instant answers |
| 🔍 **Source Attribution** | Every answer cites the exact document it came from |
| 🧠 **History-Aware** | Remembers last 10 messages for follow-up questions |
| 🛡️ **Medical Guardrails** | Strictly answers from provided context — no hallucinations |
| 💎 **Premium UI** | Modern glassmorphic interface built for clarity |
| 🔒 **Privacy First** | Document vectorization happens locally on the server |

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Backend** | FastAPI | High-performance async API server |
| **LLM** | Groq — Llama 3.3 70B | Near-instant AI responses via LPUs |
| **RAG Framework** | LangChain | Orchestrates documents, retrieval & LLM |
| **Embeddings** | HuggingFace `all-MiniLM-L6-v2` | Local, lightweight text vectorization |
| **Vector Store** | FAISS | Fast similarity search across document chunks |
| **Frontend** | HTML5 / CSS3 / Vanilla JS | Glassmorphic UI dashboard |

---

## ⚙️ How It Works

When you upload a document, the RAG pipeline processes it in 4 stages:

```
📄 PDF Upload
     │
     ▼
🔪 Chunking          → Splits text into 1,000-char chunks (100-char overlap)
     │
     ▼
🔢 Embedding         → Converts each chunk into a semantic vector
     │
     ▼
🗄️ Vector Store      → Stores vectors in FAISS for fast retrieval
     │
     ▼
❓ User Query        → Finds top 5 relevant chunks → Sends to Groq LLM
     │
     ▼
💬 Answer + Sources  → Response with document citations
```

---

## 📁 Project Structure

```
medimind/
├── app/
│   ├── main.py               # FastAPI backend — routes, uploads, sessions
│   └── templates/
│       └── index.html        # Glassmorphic frontend dashboard
│
├── logic/
│   └── rag_pipeline.py       # Core RAG logic — embeddings, retrieval chain
│
├── storage/
│   ├── uploads/              # Temporary PDF storage (gitignored)
│   └── vectorstore/          # FAISS index storage (gitignored)
│
├── .env.example              # Environment variable template
├── .gitignore
├── requirements.txt
├── setup.bat                 # One-time environment setup
└── run.bat                   # App launcher (Flask or FastAPI)
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Git

### 1. Clone the repository
```bash
git clone https://github.com/Harika-Satti/Medimind-Rag-Langchain.git
cd Medimind-Rag-Langchain
```

### 2. Set up environment variables
```bash
copy .env.example .env
```
Then open `.env` and add your API keys (see [Environment Variables](#-environment-variables)).

### 3. Install dependencies & launch
```bash
# Run once to set up virtual environment
setup.bat

# Launch the app
run.bat
```

Then open your browser at:
- **FastAPI**: `http://127.0.0.1:8000`
- **Flask**: `http://127.0.0.1:5000`

---

## 🔑 Environment Variables

Create a `.env` file based on `.env.example`:

```env
GROQ_API_KEY=your_groq_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

| Variable | Where to get it |
|---|---|
| `GROQ_API_KEY` | [console.groq.com](https://console.groq.com) |
| `GEMINI_API_KEY` | [aistudio.google.com](https://aistudio.google.com) |

> ⚠️ **Never commit your `.env` file.** It is already listed in `.gitignore`.

---

## 🤝 Contributing

Contributions are welcome! To get started:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<div align="center">
  <p>Made with ❤️ by <strong>Antigravity AI</strong></p>
  <p>⭐ Star this repo if you found it helpful!</p>
</div>
