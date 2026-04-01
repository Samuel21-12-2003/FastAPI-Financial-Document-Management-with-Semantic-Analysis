# 📄 Financial Document AI

### 🔍 RAG-based Semantic Search System

---

## 🚀 Overview

**Financial Document AI** is an AI-powered document intelligence system that enables users to upload financial documents and perform **semantic (meaning-based) search** using advanced NLP techniques.

Unlike traditional keyword search, this system understands **context and intent**, providing more accurate and relevant results.

---

## ✨ Key Features

* 📂 Upload and process financial documents (PDF)
* ✂️ Automatic text chunking for large documents
* 🔢 Embedding generation using **MiniLM (Sentence Transformers)**
* ⚡ High-speed vector search using **Qdrant**
* 🎯 Semantic search (context-aware retrieval)
* 🔄 Cross-Encoder reranking for improved accuracy
* 🔐 Secure authentication using JWT

---

## 🏗️ Tech Stack

### 🔹 Backend

* FastAPI
* Uvicorn

### 🔹 Databases

* PostgreSQL (SQLAlchemy ORM)
* Qdrant (Vector Database)

### 🔹 AI / Machine Learning

* HuggingFace Transformers
* Sentence Transformers (MiniLM)
* Cross-Encoder (MS MARCO)
* LangChain (chunking + embeddings)

### 🔹 Utilities

* PDFMiner (PDF text extraction)
* Python-dotenv (environment management)

---

## 🔄 System Architecture

### 📥 Document Processing Pipeline

1. Upload document
2. Extract text from PDF
3. Split into smaller chunks
4. Convert chunks into vector embeddings
5. Store embeddings in Qdrant

---

### 🔎 Search Pipeline

1. User submits query
2. Query is converted into embedding
3. Retrieve top similar chunks from Qdrant
4. Apply Cross-Encoder reranking
5. Return most relevant results

---

## 📂 Project Structure

```
app/
│
├── main.py              # FastAPI application entry point
├── core/               # Configuration & environment settings
├── routes/             # API route definitions
├── services/           # Business logic (RAG pipeline)
├── models/             # Database models
├── vector_db/          # Qdrant client setup
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```
git clone <your-repo-link>
cd Financial-Document-AI
```

---

### 2️⃣ Create Virtual Environment

```
python -m venv .venv
```

Activate (Windows):

```
.venv\Scripts\activate
```

---

### 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

---

### 4️⃣ Run Application

```
uvicorn app.main:app --reload
```

---

### 5️⃣ Access API Docs

```
http://127.0.0.1:8000/docs
```

---

## 🔐 Authentication

* JWT-based authentication is implemented
* Secure endpoints require user login

---

## 📊 API Endpoints

| Method | Endpoint              | Description                   |
| ------ | --------------------- | ----------------------------- |
| POST   | `/auth/login`         | User login                    |
| POST   | `/documents/upload`   | Upload document               |
| POST   | `/rag/index-document` | Index document into vector DB |
| POST   | `/rag/search`         | Perform semantic search       |

---

## 🎯 Why This Project?

Traditional search systems rely on exact keyword matching, which often leads to irrelevant results.

This project solves that by:

* Understanding semantic meaning
* Improving retrieval accuracy
* Enhancing user experience with intelligent search

---

## 🚀 Future Enhancements

* 🤖 LLM-based answer generation (ChatGPT-style responses)
* 🔀 Hybrid search (BM25 + vector search)
* 🌐 Frontend dashboard (React)
* 📊 Multi-document comparison
* 🔐 Role-based access control

---

## 👨‍💻 Author

**Samuel Pallikonda**

---

## ⭐ Key Highlights

* Implements **Retrieval-Augmented Generation (RAG)**
* Uses **Vector Database (Qdrant)** for scalable search
* Combines **semantic search + reranking** for high accuracy

---

> 💡 This project demonstrates practical application of AI in document intelligence and real-world information retrieval systems.
