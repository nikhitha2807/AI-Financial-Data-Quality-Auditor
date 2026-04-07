# DataGuardian AI — Automated Data Quality Assessment with LLMs

DataGuardian AI is a production-grade enterprise data platform that automatically analyzes datasets, detects quality issues, and provides intelligent explanations using Generative AI. It features a RAG-powered chatbot for interactive data exploration.

## 🚀 Features

- **Automated Data Profiling:** Instant statistics (row/column counts, missing values, duplicates).
- **Quality Scoring:** Overall quality score (0-100) based on Completeness, Uniqueness, and Validity.
- **AI-Driven Insights:** LLM-powered analysis using Groq (Llama 3) to explain issues and suggest cleaning steps.
- **RAG Chatbot:** Ask questions about your dataset using a Retrieval-Augmented Generation interface.
- **Modern Dashboard:** Stunning glassmorphism UI built with React and Tailwind-inspired Vanilla CSS.

## 🛠️ Tech Stack

- **Backend:** Python, FastAPI, Pandas, Pandera
- **AI/LLM:** Groq API, Llama 3
- **Vector DB:** ChromaDB
- **Frontend:** React, Lucide Icons, Recharts, Framer Motion

## 📦 Installation

### Prerequisites
- Python 3.9+
- Node.js 18+
- Groq API Key (Get it from [console.groq.com](https://console.groq.com/))

### 1. Backend Setup
```bash
cd data-guardian-ai
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file for configuration
echo "GROQ_API_KEY=your_groq_api_key_here" > .env
```

### 2. Frontend Setup
```bash
cd frontend
npm install
```

## 🏃‍♂️ Running the System

### Start Backend
```bash
# From the project root
uvicorn backend.api.app:app --reload
```
The backend will run at `http://localhost:8000`.

### Start Frontend
```bash
# In a new terminal, from the frontend directory
npm run dev
```
The frontend will run at `http://localhost:5173`.

## 📂 Project Structure
```text
data-guardian-ai/
├── backend/
│   ├── api/             # FastAPI App & Routes
│   ├── data_quality/    # Profiling & Scoring Logic
│   ├── llm/             # Groq API Integration
│   ├── chatbot/         # RAG Implementation
│   ├── database/        # ChromaDB Vector Store
│   └── datasets/        # Sample datasets
├── frontend/            # React Dashboard
└── tests/               # Unit & Integration tests
```

---
Built with ❤️ by Antigravity AI
