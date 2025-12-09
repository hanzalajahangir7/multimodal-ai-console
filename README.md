# Multi-Modal Intelligence Console (MMIC)

Enterprise-grade AI system with image, audio, text analysis, RAG chat, and PDF reporting using OpenAI, FastAPI, Streamlit, and ChromaDB.

## Features

- **Multi-Modal Analysis**: Image (GPT-4o Vision), Audio (Whisper), Text processing
- **RAG Chat**: Context-aware conversations with vector memory
- **PDF Reports**: Professional report generation
- **Vector Database**: ChromaDB for intelligent retrieval
- **Persistent Storage**: SQLite for chat history and metadata

## Tech Stack

- **Backend**: FastAPI (async REST API)
- **Frontend**: Streamlit
- **AI**: OpenAI GPT-4o, Whisper, Embeddings
- **Database**: SQLite + ChromaDB
- **Deployment**: Vercel + Streamlit Cloud

## Quick Start

1. **Install dependencies**
```bash
pip install -r requirements.txt
```

2. **Set up environment**
```bash
# Create .env file
OPENAI_API_KEY=your_key_here
```

3. **Run locally**
```bash
# Terminal 1 - Backend
python -m uvicorn src.main:app --reload

# Terminal 2 - Frontend
python -m streamlit run frontend/app.py
```

4. **Access**: Open http://localhost:8501

## Deployment

**Backend (Vercel)**
```bash
vercel
```

**Frontend (Streamlit Cloud)**
- Push to GitHub
- Deploy on https://share.streamlit.io
- Set `API_URL` environment variable

## Project Structure

```
├── src/
│   ├── api/          # FastAPI routes
│   ├── services/     # Business logic
│   ├── db/           # Database & vector store
│   └── models/       # Data models
├── frontend/         # Streamlit UI
└── data/            # Storage (uploads, DB)
```

## License

MIT
