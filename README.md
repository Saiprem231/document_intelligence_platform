# DocIntel: Intelligent Document RAG Platform 📚✨

**DocIntel** is a high-performance, full-stack Document Intelligence Platform. It enables users to explore a library of documents and interact with them using a sophisticated RAG (Retrieval-Augmented Generation) pipeline. 

Developed as a comprehensive technical assessment, this platform bridges the gap between raw data and actionable intelligence using modern AI and vector search technologies.

---

## 📸 Platform Preview

| Library Dashboard | AI Q&A Assistant (Cached) |
|<img width="977" height="906" alt="UI_1" src="https://github.com/user-attachments/assets/896cf2f8-839b-4ff8-ac66-4bcbaa4fee1d" />
<img width="738" height="820" alt="U1_2" src="https://github.com/user-attachments/assets/c16d43e4-637d-4408-b3e2-16c0a3e55c4c" />
<img width="733" height="926" alt="UI_3" src="https://github.com/user-attachments/assets/8cf687c7-4b24-461d-acbe-fbced61ca9a6" />
<img width="747" height="916" alt="UI_4" src="https://github.com/user-attachments/assets/12a6bef5-8639-4884-b320-f46b32ddc1d9" />


> **Note:** Observe the `⚡ [CACHED RESPONSE]` flag in the chat interface, which confirms the activation of the database caching layer for optimized performance.

---

## 🚀 Key Features & Bonus Implementations

### 🧠 Intelligent RAG Chat
- **Context-Aware Engine:** Powered by **Groq Llama 3.1**, the system provides precise answers based strictly on the retrieved document context.
- **Hallucination Guardrails:** Explicitly engineered prompts prevent the AI from fabricating information outside the provided library.
- **Conversational Memory (Bonus):** The system maintains the state of the conversation, allowing for natural, multi-turn follow-up questions.

### ⚡ Performance & Optimization
- **Database-Level Caching (Bonus):** Implemented a custom hashing mechanism using Django's DB cache. Identical queries are served instantly from the database, bypassing API latency and costs.
- **Vector Search:** Integrated **ChromaDB** with semantic embeddings (`sentence-transformers`) for high-accuracy document retrieval.

### 🎨 Premium UI/UX (Bonus)
- **Modern Tech Stack:** Built with **React 18** and **Vite** for a lightning-fast frontend.
- **Tailwind CSS Design:** A professional, responsive interface featuring gradient navigation, loading skeletons, and animated chat components.

---

## 🛠️ Technical Stack

- **Frontend:** React.js, Tailwind CSS, Vite, Axios.
- **Backend:** Django, Django REST Framework.
- **AI/ML:** Groq Cloud API, ChromaDB, Sentence-Transformers.
- **Database:** MySQL (Application Data & Cache) & SQLite (Vector Store).
- **Ingestion:** Selenium-based web scraping and local file processing.

---

## ⚙️ Installation & Setup

### 1. Prerequisites
- Python 3.9+
- Node.js & npm
- Groq API Key

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Create the specific caching table
python manage.py createcachetable

# Run database migrations
python manage.py migrate

# Start the Django server
python manage.py runserver


3. Frontend Setup
Bash

# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the Vite development server
npm run dev
📂 Project Structure
Plaintext

document-intelligence-platform/
├── backend/
│   ├── api/               # API views and RAG logic (services.py)
│   ├── scripts/           # Ingestion and Vector DB setup scripts
│   ├── core/              # Project settings and configuration
│   └── requirements.txt   # Backend dependencies
├── frontend/
│   ├── src/               # React components and pages
│   ├── public/            # Static assets and screenshots
│   └── package.json       # Frontend dependencies
├── chroma_db/             # Persistent Vector Database
└── README.md              # Project documentation
🏆 Requirements Checklist
[x] Full-stack application integration

[x] Selenium Data Ingestion

[x] RAG Pipeline with Llama 3.1

[x] BONUS: Multi-turn Chat History

[x] BONUS: Database-level AI Response Caching

[x] BONUS: Premium Tailwind UI

[x] BONUS: Loading states & polished UX
