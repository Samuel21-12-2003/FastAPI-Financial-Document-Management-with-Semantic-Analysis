# 📄 Financial Document AI (RAG-based Search System)

## 🚀 Overview

This project is an AI-powered **Financial Document Search System** built using **FastAPI, Qdrant, and HuggingFace embeddings**.

It allows users to:

* Upload financial documents (PDFs)
* Convert them into structured vector embeddings
* Perform **semantic search** (meaning-based search, not keyword-based)
* Retrieve the most relevant document chunks using **RAG (Retrieval-Augmented Generation)**

---

## 🧠 Key Features

* 📂 Document Upload & Processing
* ✂️ Intelligent Text Chunking
* 🔢 Embedding Generation using MiniLM
* ⚡ Fast Vector Search using Qdrant
* 🎯 Semantic Search (context-aware retrieval)
* 🔄 Cross-Encoder Reranking for improved accuracy
* 🔐 JWT-based Authentication system

---

## 🏗️ Tech Stack

### Backend

* FastAPI
* Uvicorn

### Database

* PostgreSQL (via SQLAlchemy)
* Qdrant (Vector Database)

### AI / ML

* HuggingFace Transformers
* Sentence Transformers (MiniLM)
* Cross-Encoder (MS MARCO model)
* LangChain (for embeddings & chunking)

### Others

* PDFMiner (PDF text extraction)
* Python-dotenv (environment variables)

---

## 🔄 System Architecture

### Document Processing Flow

1. User uploads a document
2. Text is extracted from the file
3. Document is split into smaller chunks
4. Each chunk is converted into vector embeddings
5. Embeddings are stored in Qdrant

---

### Search Flow

1. User enters a query
2. Query is converted into embedding
3. Top similar chunks are retrieved from Qdrant
4. Cross-Encoder reranks results for better relevance
5. Top results are returned to the user

---

## 📂 Project Structure

```
app/
│
├── main.py                # FastAPI entry point
├── core/                 # Config and settings
├── routes/               # API endpoints
├── services/             # Business logic (RAG pipeline)
├── models/               # Database models
├── vector_db/            # Qdrant connection
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```
git clone <your-repo-link>
cd Financial-Document-AI
```

---

### 2. Create virtual environment

```
python -m venv .venv
```

Activate:

```
.venv\Scripts\activate   (Windows)
```

---

### 3. Install dependencies

```
pip install -r requirements.txt
```

---

### 4. Run the server

```
uvicorn app.main:app --reload
```

---

### 5. Open API Docs

```
http://127.0.0.1:8000/docs
```

---

## 🔐 Authentication

* JWT-based authentication is implemented
* Users must login to access document upload and search endpoints

---

## 📊 Example API Endpoints

* `POST /auth/login` → User login
* `POST /documents/upload` → Upload document
* `POST /rag/index-document` → Index document into vector DB
* `POST /rag/search` → Perform semantic search

---

## 🎯 Why This Project?

Traditional search relies on keywords.
This system uses **semantic understanding**, allowing it to:

* Understand user intent
* Retrieve contextually relevant results
* Improve accuracy using reranking

---

## 🚀 Future Improvements

* Add LLM-based answer generation (ChatGPT-style responses)
* Hybrid Search (BM25 + Vector Search)
* Frontend dashboard (React)
* Multi-document comparison
* Role-based access control

---

## 🧑‍💻 Author

**Samuel Pallikonda**

---

## ⭐ Final Note

This project demonstrates a real-world implementation of:

* Retrieval-Augmented Generation (RAG)
* Vector Databases
* Semantic Search Systems

It is designed to solve practical problems in document intelligence and information retrieval.
