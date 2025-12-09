import os
from dotenv import load_dotenv

# Load .env file if it exists (for local development)
load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Use /tmp for Vercel serverless (writable directory)
    # Check if running on Vercel
    IS_VERCEL = os.getenv("VERCEL") == "1"
    
    if IS_VERCEL:
        # Vercel serverless - use /tmp (ephemeral but writable)
        DATABASE_URL = "sqlite:////tmp/app.db"
        VECTOR_DB_PATH = "/tmp/vector_db"
        UPLOAD_DIR = "/tmp/uploads"
    else:
        # Local development
        DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/app.db")
        VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "./data/vector_db")
        UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./data/uploads")

    @staticmethod
    def ensure_dirs():
        try:
            os.makedirs(config.UPLOAD_DIR, exist_ok=True)
            if hasattr(config, 'VECTOR_DB_PATH'):
                os.makedirs(config.VECTOR_DB_PATH, exist_ok=True)
        except Exception as e:
            print(f"Warning: Could not create directories: {e}")

config = Config()
config.ensure_dirs()
