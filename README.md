# HR-Intelligence-Q&A-system

**HR-Intelligence-Agent** is an AI-powered HR assistant that connects to ZKTeco biometric devices to extract and analyze employee attendance data. It supports natural language queries, generates statistical insights from the HR database, and provides a secure, scalable foundation for intelligent attendance and identity management.

---

## ⚙️ Tech Stack

- **Frontend**:  
  - Streamlit – For building the interactive web interface and dashboard.

- **Backend / Logic**:  
  - FastAPI – High-performance backend for HR functionalities.  
  - FastMCP – Model Context Protocol built over SSE for real-time event streaming.  
  - Groq LLM API – Uses `llama3-70b-8192` model for natural language understanding.  
  - MySQL – Relational database for storing employee and attendance data.  
  - ZK Library – Python SDK to connect with ZKTeco biometric attendance devices.

- **RAG (Retrieval-Augmented Generation)**:  
  - SentenceTransformers – For semantic embeddings.  
  - **Model Used**: `all-MiniLM-L6-v2` – Lightweight and efficient transformer for encoding schema text.  
  - FAISS – Facebook AI Similarity Search for fast vector indexing and retrieval.

---

## 📁 Project Structure

- **HR-INTELLIGENCE-AGENT/**
  - **rag/**
    - `auto_schema_extractor.py` – Auto-generates schema from data
    - `db_schema.md` – Markdown file describing DB schema
    - `doc_chunks.txt` – Schema chunks saved after splitting
    - `embedder.py` – Embeds schema and creates FAISS index
    - `retriever.py` – Retrieves top match from vector store
    - `update_rag.py` – Updates the FAISS store and schema chunks
    - `vector_store.faiss` – Stored FAISS index for semantic search
  - `.env` – Environment configuration file
  - `.gitignore` – Specifies intentionally untracked files to ignore
  - `app.py` – Streamlit app to visualize and interact with the system
  - `Connect_zkteco.py` – Script to connect and communicate with ZKTeco device
  - `mcp_client.py` – Client-side handler for MCP over SSE
  - `query_llm.py` – Query interface (e.g., for integrating with LLM)
  - `README.md` – Project documentation
  - `requirements.txt` – List of Python dependencies
  - `run_all.py` – Script to launch all components
  - `server.py` – FastAPI backend server
  - `TCP_port_test.py` – Tool to test if target TCP port is reachable

---

## Features – HR INTELLIGENCE AGENT

- **Real-Time Attendance Monitoring**  
  Connects to ZKTeco biometric devices by **ZK** library and interact with real-time attendance data using **FastMCP** over **SSE (Server-Sent Events)** after storing into mysql database.

- **Streamlit Dashboard**  
  A user-friendly web interface to:
  - Visualize attendance logs and metadata  
  - View results from backend analysis

- **ZKTeco SDK Integration**  
  Uses Python ZK library to:
  - Connect to attendance devices via IP and port  
  - Retrieve user and attendance logs  

- **Configurable via `.env` File**  
  - Easily configure ZKTeco host, port, and credentials - via environment variables for flexible deployment.

---

## How to Run Locally


### 1. Python version

```bash
 3.11.9
```

### 2. Clone the Repository

```
git clone "https://gitlab.com/cloudlyio/hr-intelligence-agent.git"
```

### 3. Set Up a Virtual Environment

```
python -m venv myenv
myenv\Scripts\activate
```

### 4. Install Dependencies

```
pip install -r requirements.txt
```

### 5. Set Environment Variables (Optional)

The `.env` file is used to store sensitive configuration values (e.g., API keys, passwords) securely. It should be listed in `.gitignore` to prevent accidental exposure when pushing to GitHub. Example: storing an API key in `.env`.

```
GROQ_API_KEY = your_groq_api_key
```

### 6. Run the full project

This file runs several files :  `server.py` (A wrapped mcp server with FastAPI) , `mcp_client.py`, `rag/update_rag.py` (Rag) , `app.py` (Streamlit fronted)

```bash
python run_all.py
```
